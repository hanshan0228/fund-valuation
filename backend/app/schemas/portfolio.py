from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class PortfolioResponse(PortfolioBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
