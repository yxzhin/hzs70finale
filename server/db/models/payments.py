from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from server.db.db_session import SqlAlchemyBase


class Payment(SqlAlchemyBase):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=False)
    payer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)

    expense = relationship("Expense", back_populates="payments")
    payer = relationship("User", back_populates="payments")

    def to_dict(self):
        return {
            "id": self.id,
            "expense_id": self.expense_id,
            "payer_id": self.payer_id,
            "amount": self.amount
        }
