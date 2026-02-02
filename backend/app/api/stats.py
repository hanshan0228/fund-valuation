from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Portfolio
from ..schemas.stats import RealtimeStats, HistoryStats
from ..services.stats_service import stats_service

router = APIRouter(prefix="/api/portfolios", tags=["stats"])


@router.get("/{portfolio_id}/realtime", response_model=RealtimeStats)
async def get_realtime_stats(portfolio_id: int, db: Session = Depends(get_db)):
    """获取实时收益统计"""
    # 检查组合是否存在
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="组合不存在")

    stats = await stats_service.calculate_realtime_stats(db, portfolio_id)
    return stats


@router.get("/{portfolio_id}/history", response_model=HistoryStats)
def get_history_stats(
    portfolio_id: int,
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """获取历史收益统计"""
    # 检查组合是否存在
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="组合不存在")

    stats = stats_service.get_history_stats(db, portfolio_id, days)
    return stats
