from flask import Flask, send_from_directory
from backend.api import bp as api_bp
import os
from dotenv import load_dotenv
from backend.extensions import cors
import json

if os.environ.get("PRODUCTION") != "true":
    load_dotenv(".env.development")
else:
    load_dotenv(".env.production")
    
def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    isProd = os.environ.get("PRODUCTION", "false").lower() == "true"
    print(isProd)
    app = Flask(
        __name__,
        static_folder=os.path.join(BASE_DIR + "/backend", "static", "prod" if isProd else "dev", "dist"),
        static_url_path=""
    )

    if isProd:
        cors.init_app(app, origins=["https://shareevents-production.up.railway.app"])
    else:
        cors.init_app(app, origins=[
            "https://localhost:5173",
            "https://127.0.0.1:5173",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5000",
            "http://localhost:5000"
        ],
        supports_credentials=True)

    # Register blueprints
    app.register_blueprint(api_bp)

    @app.route('/.well-known/assetlinks.json')
    def assetlinks():
        response = send_from_directory(BASE_DIR, '.well-known/assetlinks.json', mimetype='application/json')
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response

    @app.route('/photo_uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory('photo_uploads', filename)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_react(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, "index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=not os.environ.get("PRODUCTION", "false").lower() == "true")