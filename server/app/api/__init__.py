from flask import Blueprint
from server.app.api.user import user_api_bp, test_bp

api_bp = Blueprint(
    "api",
    __name__
)

api_bp.register_blueprint(user_api_bp)
api_bp.register_blueprint(test_bp)
