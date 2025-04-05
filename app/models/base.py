from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class InvestmentBaseModel(Base):
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('0 <= invested_amount <= full_amount')
    )

    def __repr__(self):
        return (
            f'Full amount = {self.full_amount}, '
            f'Invested amount = {self.invested_amount}, '
            f'Fully invested = {self.fully_invested}, '
            f'Created on - {self.create_date}, '
            f'Closed on - {self.close_date}'
        )
