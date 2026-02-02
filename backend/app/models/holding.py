from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    fund_code = Column(String(20), nullable=False, index=True)
    fund_name = Column(String(200), nullable=True)
    shares = Column(Numeric(15, 2), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    cost_nav = Column(Numeric(10, 4), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # 关系
    portfolio = relationship("Portfolio", back_populates="holdings")

    # 唯一约束
    __table_args__ = (
        UniqueConstraint('portfolio_id', 'fund_code', name='uq_portfolio_fund'),
    )
