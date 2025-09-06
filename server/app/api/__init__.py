from flask import Blueprint
from server.app.api.user import user_bp
from server.app.api.test import test_bp


api_bp = Blueprint(
    "api",
    __name__
)

api_bp.register_blueprint(user_bp)
api_bp.register_blueprint(test_bp)
