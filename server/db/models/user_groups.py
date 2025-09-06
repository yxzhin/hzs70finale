from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from server.db.db_session import SqlAlchemyBase


class UserGroup(SqlAlchemyBase):
    __tablename__ = 'user_groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)

    user = relationship("User", back_populates="user_groups", overlaps="groups,users")
    group = relationship("Group", back_populates="user_groups", overlaps="groups,users")

