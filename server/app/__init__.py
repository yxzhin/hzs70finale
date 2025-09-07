from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    app.config.from_object("server.app.conf.Config")

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"])

    login_manager = LoginManager()
    login_manager.init_app(app)
    # //@TODO
    # login_manager.login_view = "user_api.login"

    from server.app.api import api_bp

    app.register_blueprint(api_bp)

    return app
