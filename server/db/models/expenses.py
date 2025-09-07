from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from datetime import datetime, timezone
from server.db.db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship


class Expense(SqlAlchemyBase):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("expense_categories.id"), nullable=True)
    title = Column(String(100), nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String(3), nullable=False)
    expense_type = Column(String(20), nullable=False)
    split_type = Column(String(20), nullable=False)
    payment_method = Column(String(20), nullable=False)
    periodicity = Column(Integer, nullable=True)
    next_payment_date = Column(DateTime, nullable=True)
    creation_date = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    is_paid = Column(Boolean, nullable=False)

    group = relationship("Group")
    category = relationship("ExpenseCategory")
    expense_participants = relationship("ExpenseParticipant", back_populates="expense")
    payments = relationship("Payment", back_populates="expense")
    debts = relationship("Debt", back_populates="expense")

    def to_dict(self):
        return {
            "id": self.id,
            "group_id": self.group_id,
            "category_id": self.category_id,
            "title": self.title,
            "amount": self.amount,
            "currency": self.currency,
            "expense_type": self.expense_type,
            "split_type": self.split_type,
            "payment_method": self.payment_method,
            "periodicity": self.periodicity,
            "next_payment_date": self.next_payment_date.isoformat(),
            "creation_date": self.creation_date.isoformat(),
            "is_paid": self.is_paid,
        }
