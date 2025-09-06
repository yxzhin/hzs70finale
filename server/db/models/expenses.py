from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from datetime import datetime, timezone
from server.db.db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship


class Expense(SqlAlchemyBase):
    __tablename__ = "expense"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    title = Column(String(73), nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String(3), nullable=False)
    expense_type = Column(String(20), nullable=False)
    split_type = Column(String(20), nullable=False)
    payment_method = Column(String(20), nullable=False)
    periodicity = Column(Integer, nullable=True)
    next_payment_date = Column(DateTime, nullable=False)
    creation_date = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    is_paid = Column(Boolean, nullable=False)

    group = relationship("Group")

    def to_dict(self):
        return {
            "id": self.id,
            "group_id": self.group_id,
            "title": self.title,
            "amount": self.amount,
            "currency": self.currency,
            "expense_type": self.expense_type,
            "split_type": self.split_type,
            "payment_method": self.payment_method,
            "periodicity": self.periodicity,
            "next_payment_date": self.next_payment_date,
            "creation_date": self.creation_date,
            "is_paid": self.is_paid,
        }
