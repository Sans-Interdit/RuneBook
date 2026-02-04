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
import json
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, Prefetch
from sentence_transformers import SentenceTransformer
from mistralai import Mistral

SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

# client = OpenAI(
#   base_url="https://openrouter.ai/api/v1",
#   api_key=os.getenv("LLM_KEY"),
# )

mistral = Mistral(api_key=os.getenv("LLM_KEY"))

qdrant_client = QdrantClient(url="http://localhost:6333")
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    device="cpu"
)

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

    raw = match.group()

    # Correction des JSON sur-échappés générés par LLM
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

    # mots = ["Résumé" , ]
    # if any(mot in texte for mot in mots):

    classification = mistral.chat.complete(model="ministral-8b-latest", messages=[
            {"role": "system", "content": """
Tu es un classificateur de requêtes League of Legends.

Réponds UNIQUEMENT en JSON valide (pas de markdown, pas d'explication).

Règles:
- Ta réponse DOIT être un JSON STRICTEMENT valide.
- Aucune explication.
- Aucun texte avant ou après.
- Aucun caractère échappé inutile.
- Utilise uniquement des guillemets doubles ".

Format de sortie:
{"champ": "champion_name|null", "info": "lore|spell|null"}
             
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
- Guillemets doubles obligatoires
"""},
            {"role": "user", "content": prompt},
        ],
    )

    print("class", classification.choices[0].message.content)

    formatted_json = extract_json(classification.choices[0].message.content)

    systemPrompt = f"""
Tu incarnes le personnage {character} de League of Legends : {characters[character]}
Tu dois communiquer avec les utilisateurs en respectant la personnalité, le ton et le style de {character}.
Tu aides les utilisateurs à comprendre le jeu vidéo League of Legends.
Réponds UNIQUEMENT en français de manière claire avec un maximum de 1000 caractères.
"""

    print(formatted_json, type(formatted_json.get("champ")))

    points = []
    
    if formatted_json.get("champ"):
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
                    filter=Filter(
                        must=must_conditions
                    ),
                    limit=5
                )
            ],
            query=embedding,
            limit=3
        )

        points = result.points

    else:
        query_text = f"""Question: {prompt}
Context: League of Legends explanation"""
        
        embedding = model.encode(query_text)

        result = qdrant_client.query_points(
            collection_name="lol_guides",
            query=embedding,
            limit=2
        )

        points = result.points

    if points:
        # print([point.payload["title"] for point in points])
        systemPrompt += """N'invente aucune information.
Réponds uniquement en reformulant de façon naturelle le contenu du contexte.
Chaque phrase de la réponse doit pouvoir être rattachée à une phrase précise du contexte.
Si ce n’est plus possible, arrête la réponse.
N'essaie pas d'enrichir les données avec des informations supplémentaire entre parenthèses.
Ne traduis jamais les termes techniques de League of Legends, si un mot te semble propre à League of Legends, exprime le uniquement en anglais.
Si le contexte ne contient pas d’éléments permettant de répondre à la question, réponds uniquement par une excuse."""

        context_texts = [
            point.payload.get("content") or point.payload.get("text")
            for point in points
        ]
        # TODO : save personnalités?
        context = "\n".join(context_texts)
        # print(context)
        systemPrompt += f"\n\nContexte : {context}"

    print("systemPrompt : " + systemPrompt)

    response = mistral.chat.complete(model="ministral-8b-latest", messages=[
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
    character = data.get("character")
    date_now = datetime.datetime.now()
    new_conv = Conversation(name=title, character=character, updated_at=date_now, id_account=user_id)
    db_session.add(new_conv)
    db_session.commit()
    return {"message": "Conversation added", "id": new_conv.id_conversation}

@router.get("/get-conv")
async def get_conv(character: str, user_id: int = Depends(get_current_user)):
    """
    Retrieve all conversations for the current user, ordered by last updated.

    Args:
        user_id (int): Current user ID injected by dependency.

    Returns:
        list: List of dictionaries representing each conversation.
    """
    convs = db_session.query(Conversation).filter_by(id_account=user_id).filter_by(character=character).order_by(Conversation.updated_at.desc()).all()
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
    print(id_conv, message, role)
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