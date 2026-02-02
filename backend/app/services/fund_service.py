import aiohttp
import asyncio
import re
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from ..config import settings


class FundService:
    def __init__(self):
        self.cache: Dict[str, Dict] = {}
        self.cache_timestamps: Dict[str, datetime] = {}
        self.semaphore = asyncio.Semaphore(5)  # 并发限制
        self.failure_count = 0
        self.circuit_breaker_until: Optional[datetime] = None

    def _is_trading_time(self) -> bool:
        """判断是否交易时间"""
        now = datetime.now()
        if now.weekday() >= 5:  # 周六日
            return False
        hour, minute = now.hour, now.minute
        time_minutes = hour * 60 + minute
        return 570 <= time_minutes <= 900  # 9:30-15:00

    def _get_cache_ttl(self) -> int:
        """根据交易时间返回缓存TTL"""
        if self._is_trading_time():
            return 300  # 交易时间5分钟
        return 3600  # 非交易时间1小时

    def _is_cache_valid(self, fund_code: str) -> bool:
        """检查缓存是否有效"""
        if fund_code not in self.cache:
            return False
        cache_time = self.cache_timestamps.get(fund_code)
        if not cache_time:
            return False
        ttl = self._get_cache_ttl()
        return (datetime.now() - cache_time).total_seconds() < ttl

    async def _fetch_from_api(self, session: aiohttp.ClientSession, fund_code: str) -> Optional[Dict]:
        """从天天基金API获取数据"""
        # 熔断检查
        if self.circuit_breaker_until and datetime.now() < self.circuit_breaker_until:
            return None

        url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"

        async with self.semaphore:
            try:
                await asyncio.sleep(0.2)  # 请求间隔200ms
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=settings.FUND_API_TIMEOUT)) as response:
                    if response.status == 200:
                        text = await response.text()
                        # 解析jsonp: jsonpgz({...})
                        match = re.search(r'jsonpgz\((.*?)\)', text)
                        if match:
                            data = json.loads(match.group(1))
                            self.failure_count = 0  # 重置失败计数
                            return {
                                "fund_code": data.get("fundcode"),
                                "fund_name": data.get("name"),
                                "last_nav": Decimal(data.get("dwjz", "0")),
                                "estimated_nav": Decimal(data.get("gsz", "0")),
                                "estimated_growth_rate": Decimal(data.get("gszzl", "0")),
                                "estimated_time": data.get("gztime"),
                                "last_nav_date": data.get("jzrq")
                            }
            except Exception as e:
                print(f"获取基金 {fund_code} 失败: {e}")
                self.failure_count += 1
                if self.failure_count >= 3:
                    # 触发熔断
                    self.circuit_breaker_until = datetime.now() + timedelta(minutes=10)
                    print("API熔断触发，暂停10分钟")
                return None

    async def get_fund_realtime(self, fund_code: str) -> Optional[Dict]:
        """获取单个基金实时数据"""
        # 检查缓存
        if self._is_cache_valid(fund_code):
            return self.cache[fund_code]

        # 从API获取
        async with aiohttp.ClientSession() as session:
            data = await self._fetch_from_api(session, fund_code)
            if data:
                self.cache[fund_code] = data
                self.cache_timestamps[fund_code] = datetime.now()
                return data

            # 返回缓存的旧数据（如果有）
            return self.cache.get(fund_code)

    async def get_funds_realtime_batch(self, fund_codes: List[str]) -> Dict[str, Dict]:
        """批量获取基金实时数据"""
        results = {}

        # 去重
        unique_codes = list(set(fund_codes))

        async with aiohttp.ClientSession() as session:
            # 分组查询，每组10个
            for i in range(0, len(unique_codes), 10):
                batch = unique_codes[i:i+10]
                tasks = []

                for code in batch:
                    # 检查缓存
                    if self._is_cache_valid(code):
                        results[code] = self.cache[code]
                    else:
                        tasks.append(self._fetch_from_api(session, code))

                # 并发执行
                if tasks:
                    batch_results = await asyncio.gather(*tasks)
                    for j, data in enumerate(batch_results):
                        if data:
                            code = batch[j] if j < len(batch) else None
                            if code:
                                self.cache[code] = data
                                self.cache_timestamps[code] = datetime.now()
                                results[code] = data

                # 组间延迟
                if i + 10 < len(unique_codes):
                    await asyncio.sleep(0.5)

        return results

    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()
        self.cache_timestamps.clear()


# 全局实例
fund_service = FundService()
