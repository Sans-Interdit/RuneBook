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
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            data = jwt.decode(token, os.getenv("HASH_KEY"), algorithms=["HS256"])
            request.user_id = data["id"]
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

    # Verify password against stored hash
    account = session.query(Account).filter_by(email=email).first()

    if not account or not bcrypt.checkpw(password.encode("utf-8"), account.password.encode("utf-8")):
        return jsonify({"error": "Invalid credentials"}), 401
        
    return get_token(account)

def get_token(account):
    """
    Generates a JWT token for an authenticated user account.
    """
    # Create JWT payload with expiration time
    payload = {
        "id": account.id_account,
        "email": account.email,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=1),
    }

    token = jwt.encode(payload, os.getenv("HASH_KEY"), algorithm="HS256")
    return jsonify({"token": token}), 200


@bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user with an email and a hashed password.
    Returns a JWT token upon successful registration.
    """
    print("f,jsopfjopjdop")
    email = request.json.get("email")
    password = request.json.get("password")

    date_now = datetime.datetime.now()

    if not email or not password:
        print("fsdfdsfdf")
        return jsonify({"message": "Missing required fields"}), 400

    try:
        existing_user = session.query(Account).filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "Cet email est déjà utilisé"}), 409
        
        # Hash password for secure storage
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Create new account
        new_account = Account(
            email=email,
            password=hashed_password,
            created_at=date_now,
        )
        session.add(new_account)
        session.commit()

    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    return get_token(new_account)

@bp.route("/get-user-infos", methods=["GET"])
@token_required
def getinfos():
    """
    Retrieves information about an authenticated user.
    """
    userId = request.args.get("id", type=int)

    if userId:
        user = session.query(User).filter_by(id=userId).first()
    else:
        user = session.query(User).filter_by(id=request.user_id).first()
    if user:
        return (
            jsonify(
                user.getPublicData()
            ),
            200,
        )
    else:
        # User not found in database
        return jsonify({"error": "User not found"}), 404

@bp.route("/delete-user", methods=["DELETE"])
@token_required
def deleteUser():
    """
    Delete the account of an authenticated user.
    """
    user = session.query(User).filter_by(id=request.user_id).first()
    if user:
        session.delete(user)
        session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        print("User not found")
        session.rollback()
        return jsonify({"error": "User not found"}), 404

@bp.route("/change-user-infos", methods=["POST"])
@token_required
def changeInfosUser():
    """
    Change information about an authenticated user.
    """

    email = request.json.get("email")
    username = request.json.get("username")
    phone = request.json.get("phone")

    user = session.query(User).filter_by(id=request.user_id).first()

    if user:
        user.email = email
        user.username = username
        user.phone = phone
        session.commit()
        return jsonify({"message": "User information updated successfully"}), 200
    else:
        print("User not found")
        session.rollback()
        return jsonify({"error": "User not found"}), 404
    
@bp.route("/get-guides", methods=["GET"])
def getGuides():
    with Session(engine) as local_session:
        guides = local_session.query(Guide).order_by(Guide.id_guide).all()
        guides_data = [guide.to_dict() for guide in guides]
        return jsonify(guides_data), 200