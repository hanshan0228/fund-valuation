from sqlalchemy import Column, Integer, Date, Numeric, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    record_date = Column(Date, nullable=False, index=True)
    total_value = Column(Numeric(15, 2), nullable=False)
    total_cost = Column(Numeric(15, 2), nullable=False)
    daily_profit = Column(Numeric(15, 2), nullable=True)
    daily_profit_rate = Column(Numeric(6, 2), nullable=True)
    cumulative_profit = Column(Numeric(15, 2), nullable=True)
    cumulative_profit_rate = Column(Numeric(6, 2), nullable=True)
    created_at = Column(DateTime, default=func.now())

    # 关系
    portfolio = relationship("Portfolio", back_populates="history")

    # 唯一约束
    __table_args__ = (
        UniqueConstraint('portfolio_id', 'record_date', name='uq_portfolio_date'),
    )
