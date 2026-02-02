from typing import Dict, List
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy.orm import Session
from ..models import Portfolio, Holding, History
from ..schemas.stats import RealtimeStats, HoldingStats, HistoryStats, HistoryPoint
from .fund_service import fund_service


class StatsService:
    async def calculate_realtime_stats(self, db: Session, portfolio_id: int) -> RealtimeStats:
        """计算实时收益统计"""
        # 获取组合
        portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            raise ValueError(f"组合 {portfolio_id} 不存在")

        # 获取持仓
        holdings = db.query(Holding).filter(Holding.portfolio_id == portfolio_id).all()
        if not holdings:
            return RealtimeStats(
                portfolio_id=portfolio_id,
                portfolio_name=portfolio.name,
                total_cost=Decimal("0"),
                total_value=Decimal("0"),
                total_profit=Decimal("0"),
                total_profit_rate=Decimal("0"),
                holdings=[],
                updated_at=datetime.now().isoformat()
            )

        # 获取基金实时数据
        fund_codes = [h.fund_code for h in holdings]
        funds_data = await fund_service.get_funds_realtime_batch(fund_codes)

        # 计算每只基金的收益
        holding_stats_list = []
        total_cost = Decimal("0")
        total_value = Decimal("0")

        for holding in holdings:
            fund_data = funds_data.get(holding.fund_code)
            if not fund_data:
                continue

            # 计算成本净值
            cost_nav = holding.cost_nav or (holding.amount / holding.shares)

            # 当前净值（优先使用估算净值）
            current_nav = fund_data.get("estimated_nav") or fund_data.get("last_nav") or Decimal("0")

            # 持仓市值
            value = holding.shares * current_nav

            # 收益
            cost = holding.shares * cost_nav
            profit = value - cost
            profit_rate = (profit / cost * 100) if cost > 0 else Decimal("0")

            holding_stats_list.append(HoldingStats(
                fund_code=holding.fund_code,
                fund_name=fund_data.get("fund_name") or holding.fund_name or "",
                shares=holding.shares,
                cost_nav=cost_nav,
                current_nav=current_nav,
                value=value,
                profit=profit,
                profit_rate=profit_rate
            ))

            total_cost += cost
            total_value += value

        # 总收益
        total_profit = total_value - total_cost
        total_profit_rate = (total_profit / total_cost * 100) if total_cost > 0 else Decimal("0")

        return RealtimeStats(
            portfolio_id=portfolio_id,
            portfolio_name=portfolio.name,
            total_cost=total_cost,
            total_value=total_value,
            total_profit=total_profit,
            total_profit_rate=total_profit_rate,
            holdings=holding_stats_list,
            updated_at=datetime.now().isoformat()
        )

    async def record_daily_history(self, db: Session, portfolio_id: int):
        """记录每日收益历史"""
        today = date.today()

        # 检查今天是否已记录
        existing = db.query(History).filter(
            History.portfolio_id == portfolio_id,
            History.record_date == today
        ).first()

        if existing:
            print(f"组合 {portfolio_id} 今日已记录")
            return

        # 计算实时收益
        stats = await self.calculate_realtime_stats(db, portfolio_id)

        # 获取昨日记录
        yesterday_record = db.query(History).filter(
            History.portfolio_id == portfolio_id
        ).order_by(History.record_date.desc()).first()

        # 计算当日收益
        daily_profit = Decimal("0")
        daily_profit_rate = Decimal("0")
        if yesterday_record:
            daily_profit = stats.total_value - yesterday_record.total_value
            daily_profit_rate = (daily_profit / yesterday_record.total_value * 100) if yesterday_record.total_value > 0 else Decimal("0")

        # 保存记录
        history = History(
            portfolio_id=portfolio_id,
            record_date=today,
            total_value=stats.total_value,
            total_cost=stats.total_cost,
            daily_profit=daily_profit,
            daily_profit_rate=daily_profit_rate,
            cumulative_profit=stats.total_profit,
            cumulative_profit_rate=stats.total_profit_rate
        )
        db.add(history)
        db.commit()
        print(f"组合 {portfolio_id} 今日收益已记录")

    def get_history_stats(self, db: Session, portfolio_id: int, days: int = 30) -> HistoryStats:
        """获取历史收益统计"""
        portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            raise ValueError(f"组合 {portfolio_id} 不存在")

        # 查询历史记录
        history_records = db.query(History).filter(
            History.portfolio_id == portfolio_id
        ).order_by(History.record_date.desc()).limit(days).all()

        history_points = [
            HistoryPoint(
                date=record.record_date,
                total_value=record.total_value,
                total_cost=record.total_cost,
                daily_profit=record.daily_profit or Decimal("0"),
                daily_profit_rate=record.daily_profit_rate or Decimal("0"),
                cumulative_profit=record.cumulative_profit or Decimal("0"),
                cumulative_profit_rate=record.cumulative_profit_rate or Decimal("0")
            )
            for record in reversed(history_records)
        ]

        return HistoryStats(
            portfolio_id=portfolio_id,
            portfolio_name=portfolio.name,
            history=history_points
        )


# 全局实例
stats_service = StatsService()
