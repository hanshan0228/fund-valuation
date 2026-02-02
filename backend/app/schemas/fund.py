from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import datetime, date


class FundResponse(BaseModel):
    fund_code: str
    fund_name: Optional[str] = None
    last_nav: Optional[Decimal] = None
    last_nav_date: Optional[date] = None
    estimated_nav: Optional[Decimal] = None
    estimated_growth_rate: Optional[Decimal] = None
    estimated_time: Optional[datetime] = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FundRealtime(BaseModel):
    fund_code: str
    fund_name: str
    last_nav: Decimal
    estimated_nav: Decimal
    estimated_growth_rate: Decimal
    estimated_time: str
