from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


class HoldingBase(BaseModel):
    fund_code: str = Field(..., pattern=r'^\d{6}$')
    fund_name: Optional[str] = None
    shares: Decimal = Field(..., gt=0)
    amount: Decimal = Field(..., gt=0)
    cost_nav: Optional[Decimal] = None


class HoldingCreate(HoldingBase):
    pass


class HoldingUpdate(BaseModel):
    fund_name: Optional[str] = None
    shares: Optional[Decimal] = Field(None, gt=0)
    amount: Optional[Decimal] = Field(None, gt=0)
    cost_nav: Optional[Decimal] = None


class HoldingResponse(HoldingBase):
    id: int
    portfolio_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HoldingBatch(BaseModel):
    holdings: List[HoldingCreate]
