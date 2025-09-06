from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean
from server.db.db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship


class ExpenseParticipant(SqlAlchemyBase):
    __tablename__ = "expense_participants"

    id = Column(Integer, primary_key=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    percentage = Column(Float, nullable=True)
    is_paid = Column(Boolean, nullable=False, default=False)

    expense = relationship("Expense", back_populates="shares")
    user = relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "expense_id": self.expense_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "percentage": self.percentage,
            "is_paid": self.is_paid,
        }
