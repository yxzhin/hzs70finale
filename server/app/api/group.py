from flask import Blueprint, request
from flask_restful import Api, Resource
# from sqlalchemy.orm import joinedload

from server.db.db_session import create_session
from server.db.models.__all_models import User, Group, UserGroup
from server.app.utils import jwt_tokens

groups_api_bp = Blueprint(
    "groups_api",
    __name__,
    url_prefix="/groups",
)

api = Api(groups_api_bp)


class GroupResource(Resource):
    def get(self, group_id: int):
        db_sess = create_session()
        try:
            query = db_sess.query(Group)
            # //@TODO
            # query = query.options(joinedload(Group.category))
            group = query.get(group_id)

            if not group:
                return {"message": "group not found"}, 404

            return group.to_dict(users_req=True), 200

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        finally:
            db_sess.close()

    @jwt_tokens.token_required
    def post(self, user_id):
        db_sess = create_session()
        try:
            data = request.get_json()
            group_name: str = data.get("name")
            user_ids: list[int] = data.get("users")

            if not group_name or not user_ids or len(user_ids) == 0:
                return {"message": "group name and users are required"}, 400

            existing = db_sess.query(Group).filter_by(name=group_name).first()
            if existing:
                return {"message": "group already exists"}, 403

            user_owner = db_sess.get(User, user_id)
            if not user_owner:
                return {"message": "user not found"}, 404

            users = [db_sess.get(User, user_id_) for user_id_ in user_ids]
            for index, user_owner in enumerate(users):
                id_ = user_ids[index]
                if not user_owner:
                    return {"message": rf"a user with an id of {id_} not found"}, 404
                if user_ids.count(id_) > 1:
                    return {"message": f"user with id {id_} is duplicated"}, 400

            group = Group(
                name=group_name,
                owner_id=user_id
            )
            db_sess.add(group)
            db_sess.flush()

            user_groups = [
                UserGroup(
                    user_id=user_id_,
                    group_id=group.id,
                )
                for user_id_ in user_ids
            ]

            db_sess.add_all(user_groups)
            db_sess.commit()

            return {"message": "group created", "group": group.to_dict()}, 201

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        finally:
            db_sess.close()

    @jwt_tokens.token_required
    def put(self, group_id: int, user_id: int):
        db_sess = create_session()
        try:
            group = db_sess.get(Group, group_id)
            if not group:
                return {"message": "group not found"}, 404

            if group.user_id != user_id:
                return {"message": "permission denied"}, 403

            data = request.get_json()
            name: str = data.get("name")

            if name:
                group.name = name

            db_sess.commit()
            return {"message": "group updated", "group": group.to_dict()}, 200

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        finally:
            db_sess.close()

    @jwt_tokens.token_required
    def delete(self, group_id: int, user_id: int):
        db_sess = create_session()
        try:
            group = db_sess.query(Group).get(group_id)
            if not group:
                return {"message": "group not found"}, 404

            if group.user_id != user_id:
                return {"message": "permission denied"}, 403

            db_sess.delete(group)
            user_groups = db_sess.query(UserGroup).filter(group_id=group_id)
            user_groups.delete(synchronize_session=False)
            db_sess.commit()

            return {"message": "group deleted"}, 200

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        finally:
            db_sess.close()

class AllUserGroupsResource(Resource):
    @jwt_tokens.token_required
    def get(self, user_id: int):
        db_sess = create_session()
        try:
            if not user_id:
                return {"error": "'user_id' is required"}, 400

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

api.add_resource(GroupResource, "/<int:group_id>", "/")
api.add_resource(AllUserGroupsResource, "/all_user_groups")
