from flask import Blueprint, jsonify, request
from data.models import session, engine, Account, Possess, Guide, Tag, Source
from requests import get
import jwt
import bcrypt
from functools import wraps
import os
from sqlalchemy.orm import Session
import requests
import datetime

bp = Blueprint('api', __name__, url_prefix='/api')

def token_required(f):
    """
    Decorator that requires JWT authentication.
    Validates the token and checks for expiration.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        # Retrieve JWT from request headers
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            # Decode token using secret key
            data = jwt.decode(token, os.getenv("HASH_KEY"), algorithms=["HS256"])
            request.user_id = data["id"]  # Attach user ID to request
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated

@bp.route("/login", methods=["POST"])
def login():
    """
    Authenticates a user using their email and password.
    Returns a JWT token if the credentials are valid.
    """
    email = request.json.get("email")
    password = request.json.get("password")

    # Fetch user account from DB
    account = session.query(Account).filter_by(email=email).first()

    # Compare provided password with hashed password
    if not account or not bcrypt.checkpw(password.encode("utf-8"), account.password.encode("utf-8")):
        return jsonify({"error": "Invalid credentials"}), 401
        
    return get_token(account)

def get_token(account):
    """
    Generates a JWT token for an authenticated user account.
    """
    # JWT payload containing essential user data
    payload = {
        "id": account.id_account,
        "email": account.email,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=1),  # Token expires in 1 hour
    }

    token = jwt.encode(payload, os.getenv("HASH_KEY"), algorithm="HS256")
    return jsonify({"token": token}), 200


@bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user with an email and a hashed password.
    Returns a JWT token upon successful registration.
    """

    email = request.json.get("email")
    password = request.json.get("password")

    date_now = datetime.datetime.now()

    if not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    try:
        # Check if email already exists
        existing_user = session.query(Account).filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "Cet email est déjà utilisé"}), 409
        
        # Hash password before storing
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Create and save new account
        new_account = Account(
            email=email,
            password=hashed_password,
            created_at=date_now,
        )
        session.add(new_account)
        session.commit()

    except Exception as e:
        session.rollback()  # Rollback database changes on error
        print(e)
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    
    return get_token(new_account)

    
@bp.route("/get-guides", methods=["GET"])
def getGuides():
    """
    Retrieves all guides from the database.
    """
    # Use a dedicated session to prevent conflicts
    with Session(engine) as local_session:
        guides = local_session.query(Guide).order_by(Guide.id_guide).all()
        # Convert each guide object to dict for JSON response
        guides_data = [guide.to_dict() for guide in guides]
        return jsonify(guides_data), 200
