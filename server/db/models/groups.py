from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from server.db.db_session import SqlAlchemyBase


class Group(SqlAlchemyBase):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    owner_id = Column(Integer, nullable=False)

    users = relationship("User", secondary="user_groups", back_populates="groups")

    def to_dict(self, users_req=False):
        output = {
            "id": self.id,
            "name": self.name,
            "owner_id": self.owner_id,
        }

        if users_req:
            output["users"] = [user.to_dict() for user in self.users]

        return output
