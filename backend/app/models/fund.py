from sqlalchemy import Column, String, Numeric, Date, DateTime
from sqlalchemy.sql import func
from ..database import Base


class Fund(Base):
    __tablename__ = "funds"

    fund_code = Column(String(20), primary_key=True, index=True)
    fund_name = Column(String(200), nullable=True)
    last_nav = Column(Numeric(10, 4), nullable=True)
    last_nav_date = Column(Date, nullable=True)
    estimated_nav = Column(Numeric(10, 4), nullable=True)
    estimated_growth_rate = Column(Numeric(6, 2), nullable=True)
    estimated_time = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
