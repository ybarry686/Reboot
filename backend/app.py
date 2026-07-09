import os

from flask import Flask

from config import Config
from db.models import init_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BASE_DIR)


def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(REPO_ROOT, "frontend", "templates"),
        static_folder=os.path.join(REPO_ROOT, "frontend", "static"),
        static_url_path="/static",
    )
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    init_db()

    from routes.auth_routes import bp as auth_bp
    from routes.user_routes import bp as user_bp
    from routes.search_routes import bp as search_bp
    from routes.favorites_routes import bp as favorites_bp
    from routes.booking_routes import bp as booking_bp
    from routes.import_routes import bp as import_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(favorites_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(import_bp)

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)