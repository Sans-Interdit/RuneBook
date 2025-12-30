from fastapi import APIRouter, HTTPException, Depends, Request, Response, Body
from sqlalchemy.orm import Session
from data.models import engine, Account, Guide, Conversation, Message, session as db_session
import bcrypt
import datetime
import os
from huggingface_hub import InferenceClient
import jwt
from qdrant_client import QdrantClient
import re
from openai import OpenAI
import json
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, Prefetch
from sentence_transformers import SentenceTransformer

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("CHATBOT_KEY"),
)

qdrant_client = QdrantClient(url="http://localhost:6333")
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# FastAPI router
router = APIRouter()

# -------------------------
# JWT Management
# -------------------------
SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

def create_token(response: Response, account_id: int):
    """
    Create a JWT token for a user and set it as a cookie in the response.

    Args:
        response (Response): FastAPI Response object to attach the cookie.
        account_id (int): The ID of the user for whom the token is created.

    Returns:
        str: The encoded JWT token.
    """
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
    """
    Retrieve the current logged-in user ID from the JWT token in cookies.

    Args:
        request (Request): FastAPI Request object containing cookies.

    Raises:
        HTTPException: If the token is missing, expired, or invalid.

    Returns:
        int: The ID of the current user.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    try:
        payload = jwt.decode(
            token.replace("Bearer ", ""),
            SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload["id"]
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")


# -------------------------
# User Endpoints
# -------------------------
@router.post("/login")
async def login(response: Response, data: dict):
    """
    Authenticate a user with email and password, then create a JWT token.

    Args:
        response (Response): FastAPI Response object to attach JWT cookie.
        data (dict): Dictionary containing "email" and "password".

    Raises:
        HTTPException: If credentials are invalid.

    Returns:
        dict: Success message if login is successful.
    """
    email = data.get("email")
    password = data.get("password")

    account = db_session.query(Account).filter_by(email=email).first()
    if not account or not bcrypt.checkpw(password.encode("utf-8"), account.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    create_token(response, account.id_account)

    return {"message": "Login successful"}

@router.post("/register")
async def register(response: Response, data: dict):
    """
    Register a new user with email and password and create a JWT token.

    Args:
        response (Response): FastAPI Response object to attach JWT cookie.
        data (dict): Dictionary containing "email" and "password".

    Raises:
        HTTPException: If required fields are missing or email already exists.

    Returns:
        dict: Success message if registration is successful.
    """
    email = data.get("email")
    password = data.get("password")
    date_now = datetime.datetime.now()

    if not email or not password:
        raise HTTPException(status_code=400, detail="Missing required fields")

    existing_user = db_session.query(Account).filter_by(email=email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already in use")

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_account = Account(email=email, password=hashed_password, created_at=date_now)
    db_session.add(new_account)
    db_session.commit()

    create_token(response, new_account.id_account)

    return {"message": "Registration successful"}

@router.get("/logout")
async def logout(response: Response):
    """
    Logout the current user by deleting the JWT cookie.

    Args:
        response (Response): FastAPI Response object to delete JWT cookie.

    Returns:
        dict: Success message confirming logout.
    """
    response.delete_cookie(key="access_token", path="/")
    return {"message": "Logout successful"}

@router.get("/me")
async def me(user_id: int = Depends(get_current_user)):
    """
    Retrieve the current logged-in user's ID.

    Args:
        user_id (int): Injected by the `get_current_user` dependency.

    Returns:
        dict: Dictionary containing the user ID.
    """
    return {"id_user": user_id}


# -------------------------
# Guides Endpoints
# -------------------------
@router.get("/get-guides")
async def get_guides():
    """
    Retrieve all guides from the database.

    Returns:
        list: A list of dictionaries representing all guides.
    """
    with Session(engine) as local_session:
        guides = local_session.query(Guide).order_by(Guide.id_guide).all()
        return [g.to_dict() for g in guides]


# -------------------------
# Chat Endpoints
# -------------------------

def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError("Aucun JSON trouvé")
    return json.loads(match.group())

@router.post("/chat")
async def chat(data: dict):
    """
    Send a prompt to the Hugging Face chat model and return the response.

    Args:
        data (dict): Dictionary containing the "prompt" key.

    Returns:
        dict: Dictionary containing the chat model's response.
    """
    prompt = data.get("prompt")

    # mots = ["Résumé" , ]
    # if any(mot in texte for mot in mots):

    classification = client.chat.completions.create(
        model="qwen/qwen-2.5-7b-instruct",
        messages=[
            {"role": "system", "content": """
Tu es un analyseur de requêtes League of Legends.
À partir de la question utilisateur, renvoie un JSON avec :
{
  "champ": "champion concerné ou null",
  "info": "information recherchée (lore, spell, stat) ou null"
}
Ne renvoie que du JSON valide.
"""},
            {"role": "user", "content": prompt},
        ],
    )

    print(classification.choices[0].message.content)

    formatted_json = extract_json(classification.choices[0].message.content)

    systemPrompt = f"""
Tu es un assistant agissant comme un professeur bienveillant et aidant les utilisateurs à comprendre le jeu vidéo League of Legends.
Réponds en français de manière claire et concise avec un maximum de 1000 caractères.
"""
    print(formatted_json)
    
    if formatted_json.get("champ"):
        systemPrompt += """
N'invente aucune information.
Reformule les données en ta possession de maniere naturelle. 
Réponds strictement à la question posée.
Si les informations sont insuffisantes, excuse-toi et indique clairement que tu ne sais pas, sans tenter de deviner.
"""

        champ = formatted_json.get("champ")
        info = formatted_json.get("info")
        query_text = f"""
Champion: {champ}
Question: {prompt}
Context: League of Legends champion {info} explanation
        """
        embedding = model.encode(query_text)

        must_conditions = [
            FieldCondition(
                key="champion",
                match=MatchValue(value=champ)
            )
        ]

        if info:
            must_conditions.append(
                FieldCondition(
                    key="chunk_type",
                    match=MatchValue(value=info)
                )
            )


        result = qdrant_client.query_points(
            collection_name="lol_champions",
            prefetch=[
                Prefetch(
                    query=embedding,
                    filter=Filter(
                        must=must_conditions
                    ),
                    limit=3
                )
            ],
            query=embedding,
            limit=1
        )

        points = result.points

        print(points)

        if points:
            context_texts = [point.payload["text"] for point in points]
            context = "\n".join(context_texts)
            systemPrompt += f"Contexte : {context}"

        else:
            return {"response": ""}



    response = client.chat.completions.create(
        model="qwen/qwen-2.5-7b-instruct",
        messages=[
            {
                "role": "system",
                "content": systemPrompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.8,
        top_p=0.9,
        # max_tokens=200,
        # stop=["</s>", "<|endoftext|>", "<|im_end|>"]
    )


    return {"response": response.choices[0].message.content}


# -------------------------
# Conversation Endpoints
# -------------------------
@router.delete("/del-conv")
async def delete_conv(id: int, user_id: int = Depends(get_current_user)):
    """
    Delete a conversation by its ID.

    Args:
        id (int): ID of the conversation to delete.
        user_id (int): Current user ID injected by dependency.

    Raises:
        HTTPException: If the conversation does not exist.

    Returns:
        dict: Success message confirming deletion.
    """
    conv = db_session.query(Conversation).filter_by(id_conversation=id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db_session.delete(conv)
    db_session.commit()
    return {"message": "Conversation deleted"}

@router.post("/add-conv")
async def add_conv(data: dict, user_id: int = Depends(get_current_user)):
    """
    Add a new conversation for the current user.

    Args:
        data (dict): Dictionary containing "title" of the conversation.
        user_id (int): Current user ID injected by dependency.

    Returns:
        dict: Message confirming addition and the new conversation ID.
    """
    title = data.get("title")
    date_now = datetime.datetime.now()
    new_conv = Conversation(name=title, updated_at=date_now, id_account=user_id)
    db_session.add(new_conv)
    db_session.commit()
    return {"message": "Conversation added", "id": new_conv.id_conversation}

@router.get("/get-conv")
async def get_conv(user_id: int = Depends(get_current_user)):
    """
    Retrieve all conversations for the current user, ordered by last updated.

    Args:
        user_id (int): Current user ID injected by dependency.

    Returns:
        list: List of dictionaries representing each conversation.
    """
    convs = db_session.query(Conversation).filter_by(id_account=user_id).order_by(Conversation.updated_at.desc()).all()
    return [c.to_dict() for c in convs]


# -------------------------
# Messages Endpoints
# -------------------------
@router.post("/add-msg")
async def add_message(data: dict = Body(...), user_id: int = Depends(get_current_user)):
    """
    Add a new message to a conversation.

    Args:
        id_conv (int): ID of the conversation to which the message is added.
        message (str): Content of the message.
        role (str): Role of the message sender ("user" or "assistant").
        user_id (int): Current user ID injected by dependency.

    Raises:
        HTTPException: If the conversation does not exist.

    Returns:
        dict: Message confirming addition of the message.
    """
    id_conv = data.get("id_conv")
    message = data.get("message")
    role = data.get("role")

    if not id_conv or not message or not role:
        raise HTTPException(status_code=400, detail="Missing required fields")

    conv = db_session.query(Conversation).filter_by(id_conversation=id_conv).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    new_msg = Message(content=message, role=role, id_conversation=id_conv)
    db_session.add(new_msg)
    conv.updated_at = datetime.datetime.now()
    db_session.commit()
    return {"message": "Message added"}