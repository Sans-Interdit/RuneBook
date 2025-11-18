from flask import Flask, send_from_directory
from backend.api import bp as api_bp
import os
from dotenv import load_dotenv
from backend.extensions import cors
import json

isProd = os.environ.get("PRODUCTION", "false").lower() == "true"

if isProd:
    load_dotenv(".env.development")
else:
    load_dotenv(".env.production")
    
def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    app = Flask(
        __name__,
        static_folder=os.path.join(BASE_DIR + "/backend", "static", "prod" if isProd else "dev", "dist"),
        static_url_path=""
    )

    if isProd:
        cors.init_app(app, origins=["https://...................."])
    else:
        cors.init_app(app, origins=[
            "https://localhost:5173",
            "https://127.0.0.1:5173",
        ],
        supports_credentials=True)

    # Register blueprints
    app.register_blueprint(api_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=not isProd)