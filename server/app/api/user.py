from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_login import login_user

from server.db.models.users import User
from server.db.db_session import create_session
from server.app.utils import jwt_tokens

user_bp = Blueprint(
    "user_api",
    __name__,
    url_prefix="/user",
)

api = Api(user_bp)


class UserResource(Resource):
    def get(self, user_id):
        db_session = create_session()
        try:
            user = db_session.get(User, user_id)
            if not user:
                return {"message": "User not found"}, 404
            return user.to_dict(), 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
        finally:
            db_session.close()


class AllUsersResource(Resource):
    def get(self):
        db_session = create_session()
        try:
            all_users = db_session.query(User).all()
            if not all_users:
                return {"message": "User not found"}, 404
            return [user.to_dict() for user in all_users], 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
        finally:
            db_session.close()


class CurrentUserResource(Resource):
    @jwt_tokens.token_required
    def get(self, user_id, **kwargs):
        db_session = create_session()
        try:
            user = db_session.get(User, user_id)
            if not user:
                return {"message": "User not found"}, 404
            return user.to_dict(), 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
        finally:
            db_session.close()


class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"error": "Username and password required"}, 400

        db_sess = create_session()
        try:
            if db_sess.query(User).filter_by(username=username).first():
                return {"error": "User already exists"}, 400

            user = User(username=username)
            user.set_password(password)

            db_sess.add(user)
            db_sess.commit()

            login_user(user)
            token = jwt_tokens.encode_token(user.id)

            return {
                "message": "User created and logged in",
                "user": user.to_dict(),
                "token": token
            }, 201

        except Exception as e:
            return {"message": f"Error while creating user: {e}"}, 500

        finally:
            db_sess.close()


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"error": "Username and password required"}, 400

        db_sess = create_session()
        try:
            user = db_sess.query(User).filter_by(username=username).first()

            if not (user and user.check_password(password)):
                return {"error": "Invalid username or password"}, 401

            login_user(user)
            token = jwt_tokens.encode_token(user.id)

            return {
                "message": "User logged in",
                "user": user.to_dict(),
                "token": token
            }, 200

        except Exception as e:
            return {"message": f"Error while logging in: {e}"}, 500

        finally:
            db_sess.close()


api.add_resource(UserResource, "/<int:user_id>")
api.add_resource(AllUsersResource, "/all")
api.add_resource(CurrentUserResource, "/current_user")
api.add_resource(RegisterResource, "/register")
api.add_resource(LoginResource, "/login")
