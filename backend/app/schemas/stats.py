from pydantic import BaseModel
from typing import List
from decimal import Decimal
from datetime import date


class HoldingStats(BaseModel):
    fund_code: str
    fund_name: str
    shares: Decimal
    cost_nav: Decimal
    current_nav: Decimal
    value: Decimal
    profit: Decimal
    profit_rate: Decimal


class RealtimeStats(BaseModel):
    portfolio_id: int
    portfolio_name: str
    total_cost: Decimal
    total_value: Decimal
    total_profit: Decimal
    total_profit_rate: Decimal
    holdings: List[HoldingStats]
    updated_at: str


class HistoryPoint(BaseModel):
    date: date
    total_value: Decimal
    total_cost: Decimal
    daily_profit: Decimal
    daily_profit_rate: Decimal
    cumulative_profit: Decimal
    cumulative_profit_rate: Decimal


class HistoryStats(BaseModel):
    portfolio_id: int
    portfolio_name: str
    history: List[HistoryPoint]
