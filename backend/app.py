import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from backend.api import router as api_router  # = blueprint Flask

# environnement
isProd = os.environ.get("PRODUCTION", "false").lower() == "true"

if isProd:
    load_dotenv(".env.production")
else:
    load_dotenv(".env.development")

print("Production mode:", isProd)

# Create app FastAPI
def create_app() -> FastAPI:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    app = FastAPI()

    # Configurer les fichiers statiques (comme Flask static_folder)
    # static_path = os.path.join(BASE_DIR, "backend", "static", "prod" if isProd else "dist", "dev")
    # print(static_path)
    # app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

    # CORS
    if isProd:
        origins = ["https://...................."]
    else:
        origins = [
            "http://127.0.0.1:5001",
        ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routes
    app.include_router(api_router, prefix="/api")

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("backend:app", host="0.0.0.0", port=port, reload=True)



# client = OpenAI(
#   base_url="https://openrouter.ai/api/v1",
#   api_key=os.getenv("CHATBOT_KEY"),
# )

#     prompt = data.get("prompt")
#     print('vjsdfojfgpsdoj')
#     response = client.chat.completions.create(
#         model="qwen/qwen2.5-vl-32b-instruct:free",
#         messages=[
#             {
#             "role": "user",
#             "content": prompt
#             }
#         ],
#         extra_body={}
#     )
#     print(response.choices[0].message.content)
#     return {"response": response.choices[0].message.content}