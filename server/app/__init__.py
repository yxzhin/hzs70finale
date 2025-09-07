from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from server.app.utils import cron


def create_app():
    app = Flask(__name__)
    app.config.from_object("server.app.conf.Config")
    CORS(app)
    cron.init_scheduler(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    # //@TODO
    # login_manager.login_view = "user_api.login"

    from server.app.api import api_bp

    app.register_blueprint(api_bp)

    return app
