from fastapi import APIRouter, HTTPException, Depends, Request, Response, Body, status
from sqlalchemy.orm import Session
from data.models import (
    engine,
    Account,
    Guide,
    Conversation,
    Message,
    SessionLocal,
)
import bcrypt
import datetime
import os
import jwt
from qdrant_client import QdrantClient
import re
import json
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, Prefetch
from mistralai import Mistral
import requests
from pydantic import BaseModel
from typing import Literal, Optional

SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

mistral = Mistral(api_key=os.getenv("LLM_KEY"))

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_KEY"), timeout=5.0
)

API_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"
headers = {"Authorization": f"Bearer {os.getenv('HF_KEY')}"}


def embed(text):
    response = requests.post(API_URL, headers=headers, json={"inputs": text})
    return response.json()


class LoLQueryClassification(BaseModel):
    champ: str | None = None
    info: str | None = None


# FastAPI router
router = APIRouter()

characters = {
    "heimerdinger": "Heimerdinger est un scientifique yordle excentrique, méticuleux et philosophe, animé par une curiosité insatiable pour la science et l'innovation. Doté d’un esprit brillant et d’un génie technique exceptionnel, il consacre sa vie à résoudre les mystères les plus ardus de l’univers et à concevoir des inventions aussi ingénieuses que complexes.",
    "leblanc": "L’énigmatique LeBlanc est une manipulatrice maîtresse des illusions et des intrigues, figure centrale de la cabale secrète de la Rose Noire qui tire les ficelles dans l’ombre depuis des siècles. Toujours voilée et insaisissable, elle orchestre des machinations politiques et magiques à Noxus en dissimulant ses motivations derrière un masque de mystère et de duplicité, utilisant sa magie pour tromper, prédire et diriger les événements sans jamais être pleinement révélée.",
    "morgana": "Morgana est une âme tourmentée et puissante magicienne des ténèbres, déchirée entre ses origines célestes et son humanité. Ayant rejeté une justice divine rigide, elle incarne la compassion envers les souffrances humaines tout en punissant ceux qu’elle juge corrompus, cherchant à protéger les opprimés et à offrir une forme de rédemption plus nuancée que celle de sa sœur.",
    "azir": "Azir est un empereur ressuscité à l’aura majestueuse, animé par un profond sens du devoir envers la grandeur passée de Shurima. Visionnaire et déterminé, il porte l’héritage de son peuple avec fierté et autorité, aspirant à restaurer un empire prospère tout en faisant face aux trahisons et aux épreuves qui ont forgé sa destinée ancienne.",
    "shen": "Shen, l’Œil du Crépuscule, est un leader stoïque et discipliné, entièrement dédié à maintenir l’équilibre entre les mondes spirituel et matériel. Calme, réfléchi et sans préjugés, il cherche à prendre des décisions sans être influencé par ses émotions, incarnant une philosophie d’harmonie et d’exécution précise des devoirs du Kinkou, même si cela le met en conflit avec ses propres désirs personnels.",
    "ornn": "Ornn, le dieu-forgeron du Freljord, est un artisant taciturne et indépendant, préférant la solitude de sa forge volcanique au tumulte des affaires divines ou mortelles. Fier et pragmatique, il façonne des armes légendaires avec une maîtrise incomparable, intervenant rarement dans les conflits — mais toujours avec une puissance brute et un sens profond de l’artisanat authentique lorsqu’il le fait.",
    "pantheon": "Pantheon est un guerrier Rakkor au courage indomptable, forgé par la douleur, la perte et une volonté inébranlable de protéger les mortels. Stoïque et résilient, il incarne la lutte contre des forces supérieures, refusant de renier sa propre humanité ou son engagement envers ceux qui comptent sur lui, combattant avec une détermination obstinée même face à des ennemis divins.",
}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# JWT Management
# -------------------------


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
        "exp": datetime.datetime.now() + datetime.timedelta(hours=24),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    if os.getenv("PRODUCTION") == "true":
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
            max_age=3600 * 24,
        )

    else:
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
            token.replace("Bearer ", ""), SECRET_KEY, algorithms=["HS256"]
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
async def login(response: Response, data: dict, db: Session = Depends(get_db)):
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

    account = db.query(Account).filter_by(email=email).first()
    if not account or not bcrypt.checkpw(
        password.encode("utf-8"), account.password.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    create_token(response, account.id_account)

    return {"message": "Login successful", "id_account": account.id_account}


@router.post("/register")
async def register(response: Response, data: dict, db: Session = Depends(get_db)):
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

    existing_user = db.query(Account).filter_by(email=email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already in use")

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    new_account = Account(email=email, password=hashed_password, created_at=date_now)
    db.add(new_account)
    db.commit()

    create_token(response, new_account.id_account)

    return {"message": "Registration successful", "id_account": new_account.id_account}


@router.get("/logout")
async def logout(response: Response):
    """
    Logout the current user by deleting the JWT cookie.

    Args:
        response (Response): FastAPI Response object to delete JWT cookie.

    Returns:
        dict: Success message confirming logout.
    """
    if os.getenv("PRODUCTION") == "true":
        response.delete_cookie(
            key="access_token", path="/", secure=True, samesite="None"
        )
        return {"message": "Logout successful"}

    else:
        response.delete_cookie(
            key="access_token", path="/", secure=False, samesite="Lax"
        )
        return {"message": "Logout successful"}


@router.delete("/suppr-acc")
async def supprAcc(
    user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Suppress the current user account.

    Args:
        user_id (int): Injected by the `get_current_user` dependency.

    Returns:
        dict: Success message confirming suppression.
    """

    account = db.query(Account).filter_by(id_account=user_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(account)
    db.commit()
    return {"message": "Account deleted"}


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


@router.get("/get-email")
async def get_conv(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve email of the current user

    Args:
        user_id (int): Current user ID injected by dependency.

    Returns:
        str: Email of the user.
    """
    acc = db.query(Account).filter_by(id_account=user_id).first()

    return acc.email


@router.put("/change-email")
async def change_email(
    data: dict = Body(...),
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    newEmail = data.get("email")

    if not newEmail:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le champ newEmail est requis.",
        )

    email_exists = db.query(Account).filter(Account.email == newEmail).first()
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email est déjà utilisé.",
        )

    db.query(Account).filter(Account.id_account == user_id).update({"email": newEmail})
    db.commit()

    return {"message": "Account modified"}


@router.put("/change-password")
async def change_email(
    data: dict = Body(...),
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    newPassword = data.get("password")

    if not newPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le champ newPassword est requis.",
        )

    hashed_new_password = bcrypt.hashpw(
        newPassword.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    db.query(Account).filter(Account.id_account == user_id).update(
        {"password": hashed_new_password}
    )
    db.commit()

    return {"message": "Account modified"}


# -------------------------
# Guides Endpoints
# -------------------------
@router.get("/guides")
async def get_guides():
    """
    Retrieve all guides previews from the database.

    Returns:
        list: A list of dictionaries representing all guides previews.
    """
    with Session(engine) as local_session:
        guides = local_session.query(Guide).order_by(Guide.id_guide).all()
        return [g.to_dict_preview() for g in guides]


@router.get("/guides/{id}")
async def get_guides(id: int):
    """
    Retrieve all guides from the database.

    Returns:
        list: A list of dictionaries representing all guides.
    """
    with Session(engine) as local_session:
        guide = local_session.query(Guide).where(Guide.id_guide == id).first()

        if not guide:
            raise HTTPException(status_code=404, detail="Guide not found")

        return guide.to_dict_full()


# -------------------------
# Chat Endpoints
# -------------------------


def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError("Aucun JSON trouvé")

    raw = match.group()

    if '\\"' in raw:
        raw = raw.replace('\\"', '"')

    return json.loads(raw)


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
    character = data.get("character")

    classification = mistral.chat.complete(
        model="ministral-8b-latest",
        messages=[
            {
                "role": "system",
                "content": """Tu es un classificateur de requêtes League of Legends.

Format de sortie:
{"champ": "champion_name|null", "info": "lore|stats|spell|null"}
             
Exemples:
Q: "L'histoire de Yasuo"
A: {"champ": "Yasuo", "info": "lore"}

Q: "Sorts d'Ahri"
A: {"champ": "Ahri", "info": "spell"}

Q: "Meilleurs items ADC"
A: {"champ": null, "info": null}

Q: "Quel rôle joue Graves ?"
A: {"champ": "Graves", "info": "stats"}

Règles:
- "champ": nom exact du champion ou null
- "info": 
  * "lore" = histoire/background du champion
  * "spell" = compétences/capacités du champion
  * "stats" = données techniques du champion
  * null = autre requête
""",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )


    raw_content = classification.choices[0].message.content
    result = LoLQueryClassification.model_validate_json(raw_content)

    systemPrompt = f"""Interprète le personnage {character} de League of Legends : {characters[character]}
Lorsque le contexte s'y prête, tu dois communiquer avec les utilisateurs en respectant la personnalité, le ton et le style de {character}.
Tu aides les utilisateurs à comprendre le jeu vidéo League of Legends.
Réponds uniquement en reformulant de façon naturelle le contenu du contexte.
Chaque phrase de la réponse doit pouvoir être rattachée à une phrase précise du contexte.
N'invente aucune information.
Si le contexte ne contient pas d’éléments permettant de répondre à la question, réponds uniquement en s'excusant.
Réponds UNIQUEMENT en français de manière claire avec un maximum de 1000 caractères.
"""

    points = []

    if result.champ and result.info:
        champ = result.champ
        info = result.info
        query_text = f"""
Champion: {champ}
Question: {prompt}
Context: League of Legends champion {info} explanation
        """
        embedding = embed(query_text)

        must_conditions = [
            FieldCondition(key="champion", match=MatchValue(value=champ))
        ]

        if info:
            must_conditions.append(
                FieldCondition(key="chunk_type", match=MatchValue(value=info))
            )

        result = qdrant_client.query_points(
            collection_name="lol_champions",
            prefetch=[Prefetch(filter=Filter(must=must_conditions), limit=5)],
            query=embedding,
            limit=4,
        )

        points = result.points

    else:
        query_text = f"""Question: {prompt}
Context: League of Legends explanation"""

        embedding = embed(query_text)

        result = qdrant_client.query_points(
            collection_name="lol_guides", query=embedding, limit=2
        )

        points = result.points


    if points:
        systemPrompt += """N'essaie pas d'enrichir les données avec des informations supplémentaire entre parenthèses.
Ne traduis jamais les termes techniques de League of Legends, si un mot te semble propre à League of Legends, exprime le uniquement en anglais."""

        context_texts = [
            point.payload.get("content") or point.payload.get("text")
            for point in points
        ]
        context = "\n".join(context_texts)
        systemPrompt += f"\n\nContexte : {context}"

    response = mistral.chat.complete(
        model="ministral-8b-latest",
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
        top_p=0.9,
    )

    return {"response": response.choices[0].message.content}


# -------------------------
# Conversation Endpoints
# -------------------------
@router.delete("/del-conv")
async def delete_conv(
    id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
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
    conv = db.query(Conversation).filter_by(id_conversation=id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db.delete(conv)
    db.commit()
    return {"message": "Conversation deleted"}


@router.post("/add-conv")
async def add_conv(
    data: dict, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Add a new conversation for the current user.

    Args:
        data (dict): Dictionary containing "title" of the conversation.
        user_id (int): Current user ID injected by dependency.

    Returns:
        dict: Message confirming addition and the new conversation ID.
    """
    title = data.get("title")
    character = data.get("character")
    date_now = datetime.datetime.now()
    new_conv = Conversation(
        name=title, character=character, updated_at=date_now, id_account=user_id
    )
    db.add(new_conv)
    db.commit()
    return {"message": "Conversation added", "id": new_conv.id_conversation}


@router.get("/get-conv")
async def get_conv(
    character: str,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve all conversations for the current user, ordered by last updated.

    Args:
        user_id (int): Current user ID injected by dependency.

    Returns:
        list: List of dictionaries representing each conversation.
    """
    convs = (
        db.query(Conversation)
        .filter_by(id_account=user_id)
        .filter_by(character=character)
        .order_by(Conversation.updated_at.desc())
        .all()
    )
    return [c.to_dict() for c in convs]


# -------------------------
# Messages Endpoints
# -------------------------
@router.post("/add-msg")
async def add_message(
    data: dict = Body(...),
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
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

    conv = db.query(Conversation).filter_by(id_conversation=id_conv).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    new_msg = Message(content=message, role=role, id_conversation=id_conv)
    db.add(new_msg)
    conv.updated_at = datetime.datetime.now()
    db.commit()
    return {"message": "Message added"}
