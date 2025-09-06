from flask import Blueprint
from flask_restful import Api, Resource
from server.db.db_session import create_session
from server.db.models.__all_models import User, Group
from server.app.utils import jwt_tokens

user_groups_bp = Blueprint(
    "user_groups_api",
    __name__,
    url_prefix="/user_groups",
)

api = Api(user_groups_bp)


class UserGroupResource(Resource):
    @jwt_tokens.token_required
    def get(self, user_id: int):
        db_sess = create_session()
        try:
            user = db_sess.get(User, user_id)
            if not user:
                return {"message": "User not found"}, 404
            return {
                "user_id": user.id,
                "groups": [group.to_dict() for group in user.groups]
            }, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
        finally:
            db_sess.close()

    @jwt_tokens.token_required
    def post(self, user_id: int, group_id: int):
        db_sess = create_session()
        try:
            user = db_sess.get(User, user_id)
            if not user:
                return {"message": "User not found"}, 404

            group = db_sess.get(Group, group_id)
            if not group:
                return {"message": "Group not found"}, 404

            if group not in user.groups:
                user.groups.append(group)
                db_sess.commit()
                return {
                    "message": f"User {user_id} added to group {group_id}",
                    "groups": [g.to_dict() for g in user.groups]
                }, 200
            else:
                return {"message": f"User {user_id} is already in group {group_id}"}, 200

        except Exception as e:
            db_sess.rollback()
            return {"message": f"An error occurred: {str(e)}"}, 500
        finally:
            db_sess.close()

    @jwt_tokens.token_required
    def delete(self, user_id: int, group_id: int):
        db_sess = create_session()
        try:
            user = db_sess.get(User, user_id)
            if not user:
                return {"message": "User not found"}, 404

            group = db_sess.get(Group, group_id)
            if not group:
                return {"message": "Group not found"}, 404

            if group in user.groups:
                user.groups.remove(group)
                db_sess.commit()
                return {
                    "message": f"User {user_id} removed from group {group_id}",
                    "groups": [g.to_dict() for g in user.groups]
                }, 200
            else:
                return {"message": f"User {user_id} is not in group {group_id}"}, 200

        except Exception as e:
            db_sess.rollback()
            return {"message": f"An error occurred: {str(e)}"}, 500
        finally:
            db_sess.close()


api.add_resource(UserGroupResource, "/", "/<int:group_id>")
