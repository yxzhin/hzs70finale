from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from datetime import datetime, timezone
from server.db.db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship


class Expense(SqlAlchemyBase):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("expense_categories.id"), nullable=True)
    title = Column(String(100), nullable=True)
    amount = Column(Integer, nullable=True)
    currency = Column(String(3), nullable=True)
    expense_type = Column(String(20), nullable=True)
    split_type = Column(String(20), nullable=True)
    payment_method = Column(String(20), nullable=True)
    periodicity = Column(Integer, nullable=True)
    next_payment_date = Column(DateTime, nullable=True)
    creation_date = Column(DateTime, nullable=True, default=datetime.now(timezone.utc))
    is_paid = Column(Boolean, nullable=True)

    group = relationship("Group")
    category = relationship("ExpenseCategory")
    expense_participants = relationship("ExpenseParticipant", back_populates="expense")
    payments = relationship("Payment", back_populates="expense")
    debts = relationship("Debt", back_populates="expense")

    def to_dict(self, category_req=False):
        output = {
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
            "next_payment_date": self.next_payment_date.isoformat() if self.next_payment_date else None,
            "creation_date": self.creation_date.isoformat(),
            "is_paid": self.is_paid,
        }

        if category_req:
            output["category"] = self.category.to_dict() if self.category else None

        return output
