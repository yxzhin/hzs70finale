from sqlalchemy import Column, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from server.db.db_session import SqlAlchemyBase


class Debt(SqlAlchemyBase):
    __tablename__ = "debts"

    id = Column(Integer, primary_key=True)
    debtor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    creditor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=False)
    is_paid = Column(Boolean, default=False)

    expense = relationship("Expense", back_populates="debts")
    debtor = relationship("User", foreign_keys=[debtor_id])
    creditor = relationship("User", foreign_keys=[creditor_id])

    def to_dict(self):
        return {
            "id": self.id,
            "debtor_id": self.debtor_id,
            "creditor_id": self.creditor_id,
            "amount": self.amount,
            "expense_id": self.expense_id,
            "is_paid": self.is_paid
        }
