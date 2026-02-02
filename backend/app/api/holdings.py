from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal
from ..database import get_db
from ..models import Holding, Portfolio
from ..schemas.holding import HoldingCreate, HoldingUpdate, HoldingResponse, HoldingBatch

router = APIRouter(prefix="/api", tags=["holdings"])


@router.get("/portfolios/{portfolio_id}/holdings", response_model=List[HoldingResponse])
def get_holdings(portfolio_id: int, db: Session = Depends(get_db)):
    """获取持仓列表"""
    # 检查组合是否存在
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="组合不存在")

    holdings = db.query(Holding).filter(Holding.portfolio_id == portfolio_id).all()
    return holdings


@router.post("/portfolios/{portfolio_id}/holdings", response_model=HoldingResponse)
def create_holding(portfolio_id: int, holding: HoldingCreate, db: Session = Depends(get_db)):
    """添加持仓"""
    # 检查组合是否存在
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="组合不存在")

    # 检查是否已存在
    existing = db.query(Holding).filter(
        Holding.portfolio_id == portfolio_id,
        Holding.fund_code == holding.fund_code
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="该基金已存在于组合中")

    # 计算成本净值
    cost_nav = holding.cost_nav or (holding.amount / holding.shares)

    db_holding = Holding(
        portfolio_id=portfolio_id,
        **holding.model_dump(),
        cost_nav=cost_nav
    )
    db.add(db_holding)
    db.commit()
    db.refresh(db_holding)
    return db_holding


@router.post("/portfolios/{portfolio_id}/holdings/batch")
def create_holdings_batch(portfolio_id: int, batch: HoldingBatch, db: Session = Depends(get_db)):
    """批量添加持仓"""
    # 检查组合是否存在
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="组合不存在")

    created_count = 0
    skipped_count = 0

    for holding in batch.holdings:
        # 检查是否已存在
        existing = db.query(Holding).filter(
            Holding.portfolio_id == portfolio_id,
            Holding.fund_code == holding.fund_code
        ).first()

        if existing:
            skipped_count += 1
            continue

        # 计算成本净值
        cost_nav = holding.cost_nav or (holding.amount / holding.shares)

        db_holding = Holding(
            portfolio_id=portfolio_id,
            **holding.model_dump(),
            cost_nav=cost_nav
        )
        db.add(db_holding)
        created_count += 1

    db.commit()
    return {
        "message": "批量导入完成",
        "created": created_count,
        "skipped": skipped_count
    }


@router.put("/holdings/{holding_id}", response_model=HoldingResponse)
def update_holding(holding_id: int, holding_update: HoldingUpdate, db: Session = Depends(get_db)):
    """更新持仓"""
    holding = db.query(Holding).filter(Holding.id == holding_id).first()
    if not holding:
        raise HTTPException(status_code=404, detail="持仓不存在")

    update_data = holding_update.model_dump(exclude_unset=True)

    # 如果更新了金额或份额，重新计算成本净值
    if "amount" in update_data or "shares" in update_data:
        amount = update_data.get("amount", holding.amount)
        shares = update_data.get("shares", holding.shares)
        if "cost_nav" not in update_data:
            update_data["cost_nav"] = amount / shares

    for key, value in update_data.items():
        setattr(holding, key, value)

    db.commit()
    db.refresh(holding)
    return holding


@router.delete("/holdings/{holding_id}")
def delete_holding(holding_id: int, db: Session = Depends(get_db)):
    """删除持仓"""
    holding = db.query(Holding).filter(Holding.id == holding_id).first()
    if not holding:
        raise HTTPException(status_code=404, detail="持仓不存在")

    db.delete(holding)
    db.commit()
    return {"message": "删除成功"}
