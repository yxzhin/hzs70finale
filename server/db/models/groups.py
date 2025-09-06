from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from server.db.db_session import SqlAlchemyBase


class Group(SqlAlchemyBase):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user_groups = relationship("UserGroup", back_populates="group", cascade="all, delete-orphan")
    users = relationship("User", secondary="user_groups", back_populates="groups", overlaps="user_groups")
    owner = relationship("User", back_populates="owned_groups")

    def to_dict(self, users_req=False):
        output = {
            "id": self.id,
            "name": self.name,
            "owner_id": self.owner_id,
        }

        if users_req:
            output["users"] = [user.to_dict() for user in self.users]

        return output
