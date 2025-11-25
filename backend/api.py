from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from data.models import engine, Account, Guide, Conversation, session as db_session
import bcrypt
import datetime
import os
from huggingface_hub import InferenceClient
import jwt

# Charger clé Hugging Face
chatbot_key = os.getenv("KEY")
client = InferenceClient(provider="hf-inference", api_key=chatbot_key)

# Router FastAPI
router = APIRouter()

# -------------------------
# Gestion JWT
# -------------------------
SECRET_KEY = os.getenv("FLASK_SECRET_KEY")  # ou autre clé

def create_token(response: Response, account_id: int):
    payload = {
        "id": account_id,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="Lax",
        path="/",
        max_age=3600 * 24,
    )

    return token

def get_current_user(request: Request):
    # Essaye de récupérer le cookie
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token manquant")

    try:
        payload = jwt.decode(
            token.replace("Bearer ", ""),
            SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload["id"]
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token invalide")


# -------------------------
# User endpoints
# -------------------------
@router.post("/login")
async def login(response: Response, data: dict):
    email = data.get("email")
    password = data.get("password")

    account = db_session.query(Account).filter_by(email=email).first()
    if not account or not bcrypt.checkpw(password.encode("utf-8"), account.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    create_token(response, account.id_account)

    return {"message": "Login successful"}

@router.post("/register")
async def register(response: Response, data: dict):
    email = data.get("email")
    password = data.get("password")
    date_now = datetime.datetime.now()

    if not email or not password:
        raise HTTPException(status_code=400, detail="Missing required fields")

    existing_user = db_session.query(Account).filter_by(email=email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Cet email est déjà utilisé")

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_account = Account(email=email, password=hashed_password, created_at=date_now)
    db_session.add(new_account)
    db_session.commit()

    create_token(response, new_account.id_account)

    return {"message": "Registration successful"}

@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token", path="/")
    return {"message": "Logout successful"}

@router.get("/me")
async def me(user_id: int = Depends(get_current_user)):
    return {"id_user": user_id}

# -------------------------
# Guides
# -------------------------
@router.get("/get-guides")
async def get_guides():
    with Session(engine) as local_session:
        guides = local_session.query(Guide).order_by(Guide.id_guide).all()
        return [g.to_dict() for g in guides]

# -------------------------
# Chat
# -------------------------
@router.post("/chat")
async def chat(data: dict):
    prompt = data.get("prompt")
    model = "qwen/qwen3-4b:free"

    response = client.chat.model_chat(
        model=model,
        inputs=prompt,
        parameters={}
    )
    return {"response": response.generated_text}

# -------------------------
# Conversations
# -------------------------
@router.delete("/del-conv")
async def delete_conv(id: int, user_id: int = Depends(get_current_user)):
    conv = db_session.query(Conversation).filter_by(id_conversation=id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db_session.delete(conv)
    db_session.commit()
    return {"message": "Conversation deleted"}

@router.post("/add-conv")
async def add_conv(data: dict, user_id: int = Depends(get_current_user)):
    title = data.get("title")
    date_now = datetime.datetime.now()

    new_conv = Conversation(name=title, updated_at=date_now, id_account=user_id)
    db_session.add(new_conv)
    db_session.commit()
    return {"message": "Conversation added", "id": new_conv.id_conversation}