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
        db_session = create_session()
        try:
            query = db_session.query(Group)
            # //@TODO
            # query = query.options(joinedload(Group.category))
            group = query.get(group_id)

            if not group:
                return {"message": "group not found"}, 404

            return group.to_dict(users_req=True), 200

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        finally:
            db_session.close()

    @jwt_tokens.token_required
    def post(self, user_id):
        db_session = create_session()
        try:
            data = request.get_json()
            group_name: str = data.get("name")
            user_ids: list[int] = data.get("users")

            if not group_name or not user_ids or len(user_ids) == 0:
                return {"message": "group name and users are required"}, 400

            existing = db_session.query(Group).filter_by(name=group_name).first()
            if existing:
                return {"message": "group already exists"}, 403

            user = db_session.get(User, user_id)
            if not user:
                return {"message": "user not found"}, 404

            users = [db_session.get(User, user_id_) for user_id_ in user_ids]
            for index, user in enumerate(users):
                if not user:
                    id_ = user_ids[index]
                    return {"message": rf"a user with an id of {id_} not found"}, 404

            group = Group(
                name=group_name,
            )

            user_groups = [
                UserGroup(
                    user_id=user_id_,
                    group_id=group.id,
                )
                for user_id_ in user_ids
            ]

            db_session.add(group)
            db_session.add_all(user_groups)
            db_session.commit()

            return {"message": "group created", "group": group.to_dict()}, 201

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        finally:
            db_session.close()

    @jwt_tokens.token_required
    def put(self, listing_id: int, user_id: int): ...


api.add_resource(GroupResource, "/<int:listing_id>", "/")
