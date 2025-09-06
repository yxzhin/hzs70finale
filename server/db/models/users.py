from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from server.db.db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    user_groups = relationship("UserGroup", back_populates="user", cascade="all, delete-orphan")
    groups = relationship("Group", secondary="user_groups", back_populates="users", overlaps="user_groups")
    owned_groups = relationship("Group", back_populates="owner")

    def to_dict(self, groups_req=False):
        output = {
            "id": self.id,
            "username": self.username,
        }

        if groups_req:
            output["groups"] = [group.to_dict() for group in self.groups]

        return output

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
