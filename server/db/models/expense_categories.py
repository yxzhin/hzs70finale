from sqlalchemy import Column, Integer, String, ForeignKey
from server.db.db_session import SqlAlchemyBase


class ExpenseCategory(SqlAlchemyBase):
    __tablename__ = "expense_categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(73), nullable=False, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner_id": self.owner_id,
        }
