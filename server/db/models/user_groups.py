from sqlalchemy import Table, Column, Integer, ForeignKey
from server.db.db_session import SqlAlchemyBase

user_groups = Table(
    "user_groups",
    SqlAlchemyBase.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("group_id", Integer, ForeignKey("groups.id"))
)
