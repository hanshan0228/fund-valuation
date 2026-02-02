from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Portfolio
from ..schemas.portfolio import PortfolioCreate, PortfolioUpdate, PortfolioResponse

router = APIRouter(prefix="/api/portfolios", tags=["portfolios"])


@router.get("", response_model=List[PortfolioResponse])
def get_portfolios(db: Session = Depends(get_db)):
    """获取所有组合"""
    portfolios = db.query(Portfolio).all()
    return portfolios


@router.post("", response_model=PortfolioResponse)
def create_portfolio(portfolio: PortfolioCreate, db: Session = Depends(get_db)):
    """创建组合"""
    db_portfolio = Portfolio(**portfolio.model_dump())
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


@router.get("/{portfolio_id}", response_model=PortfolioResponse)
def get_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    """获取组合详情"""
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="组合不存在")
    return portfolio


@router.put("/{portfolio_id}", response_model=PortfolioResponse)
def update_portfolio(portfolio_id: int, portfolio_update: PortfolioUpdate, db: Session = Depends(get_db)):
    """更新组合"""
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="组合不存在")

    update_data = portfolio_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(portfolio, key, value)

    db.commit()
    db.refresh(portfolio)
    return portfolio


@router.delete("/{portfolio_id}")
def delete_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    """删除组合"""
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="组合不存在")

    db.delete(portfolio)
    db.commit()
    return {"message": "删除成功"}
