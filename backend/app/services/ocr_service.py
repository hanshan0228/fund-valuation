import re
import cv2
import numpy as np
from PIL import Image
from typing import List, Dict, Optional
from decimal import Decimal
import base64
import io


class OCRService:
    def __init__(self):
        self._ocr = None

    def _get_ocr(self):
        """延迟加载PaddleOCR"""
        if self._ocr is None:
            import os
            os.environ['PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK'] = 'True'
            from paddleocr import PaddleOCR
            # 使用移动端轻量模型，大幅提升速度
            self._ocr = PaddleOCR(
                use_textline_orientation=False,
                lang='ch',
                det_model_dir=None,  # 使用默认轻量模型
                rec_model_dir=None,
                ocr_version='PP-OCRv4',  # 使用v4轻量版本
            )
        return self._ocr

    def _split_long_image(self, image: np.ndarray, max_height: int = 4000) -> List[np.ndarray]:
        """将长图分割成多个小图"""
        height, width = image.shape[:2]

        if height <= max_height:
            return [image]

        # 分割图片，每段有一定重叠以避免切断文字
        overlap = 300
        segments = []
        y = 0

        while y < height:
            end_y = min(y + max_height, height)
            segment = image[y:end_y, :]
            segments.append(segment)
            y = end_y - overlap
            if end_y == height:
                break

        return segments

    def _preprocess_image(self, image: np.ndarray) -> List[np.ndarray]:
        """图片预处理，只返回原图（简化处理）"""
        # 对于长图，只使用原图策略，避免重复处理
        return [image]

    def _extract_fund_info(self, text_lines: List[str]) -> List[Dict]:
        """从OCR文本中提取基金信息"""
        results = []

        # 正则模式
        fund_code_pattern = re.compile(r'(\d{6})')

        # 基金名称必须包含的核心关键词（基金类型）
        fund_type_keywords = ['债券', '混合', '指数', '股票', 'ETF', '联接', 'LOF', 'QDII',
                              '货币', '理财', '增强', '量化', '灵活配置', '偏股', '偏债']

        # 基金名称常见后缀（用于辅助识别）
        fund_suffixes = ['A', 'B', 'C', 'D', 'E', 'F', 'R', 'H', 'I',
                         'ETF', 'LOF', 'QDII', '联接A', '联接C', '联接']

        # 基金公司名称前缀（扩充列表）
        fund_company_prefixes = ['华夏', '易方达', '广发', '南方', '博时', '富国', '招商',
                                 '汇添富', '嘉实', '鹏华', '工银', '建信', '中银', '交银',
                                 '兴全', '景顺', '天弘', '银华', '国泰', '华安', '中欧',
                                 '诺安', '平安', '大成', '申万', '长信', '华宝', '前海',
                                 '财通', '德邦', '万家', '长城', '东方', '国投', '华商',
                                 '兴业', '农银', '浦银', '民生', '永赢', '西部', '信达',
                                 '金鹰', '泰达', '国联', '中加', '融通', '新华', '光大',
                                 '摩根', '信澳', '中信', '海富通', '上投', '国海', '安信',
                                 '方正', '中邮', '创金', '九泰', '中融', '鑫元', '红塔',
                                 '睿远', '泓德', '朱雀', '淳厚', '合煦', '弘毅']

        # 排除关键词（非基金内容）
        exclude_keywords = ['降准', '降息', '影响', '锦囊', '投资建议',
                           '分析师', '观点', '策略', '研报', '解读', '热点',
                           '新闻', '资讯', '公告', '排行', '榜单',
                           '昨日', '今日', '本周', '本月', '点击', '查看', '更多',
                           '持仓金额', '持有份额', '累计收益', '持仓收益', '日收益',
                           '总金额', '总收益', '安全', '保障', '我的', '全部',
                           '自选', '关注', '加自选', '买入', '卖出',
                           '基金经理说', '限额上调', '把握', '开门红',
                           '拐点', '临近', '关注市场', '有哪些', '怎么',
                           '如何', '为什么', '什么是', '对哪', '？',
                           '!', '！', '金额/', '收益/', '份额/',
                           '金选指数', '金选债券', '金选混合', '金选纯债']

        # 第一遍：尝试找基金代码
        i = 0
        while i < len(text_lines):
            line = text_lines[i]
            code_match = fund_code_pattern.search(line)
            if code_match:
                fund_code = code_match.group(1)
                search_lines = text_lines[i:min(i+5, len(text_lines))]
                amounts = self._find_amounts_in_lines(search_lines)

                if amounts:
                    results.append({
                        "fund_code": fund_code,
                        "amount": float(max(amounts)),
                        "shares": 0.0,
                        "fund_name": ""
                    })
                i += 3
            else:
                i += 1

        # 如果没找到基金代码，第二遍：通过基金名称+金额识别
        if not results:
            i = 0
            while i < len(text_lines):
                line = text_lines[i].strip()

                # 排除明显不是基金的内容
                if any(ex in line for ex in exclude_keywords):
                    i += 1
                    continue

                # 检查是否是基金名称
                is_fund_name = self._is_fund_name(line, fund_type_keywords,
                                                   fund_suffixes, fund_company_prefixes)

                if is_fund_name:
                    fund_name = line
                    # 在后续行查找金额
                    search_lines = text_lines[i+1:min(i+4, len(text_lines))]
                    amounts = self._find_amounts_in_lines(search_lines)

                    if amounts:
                        amount = max(amounts)
                        results.append({
                            "fund_code": "",
                            "amount": float(amount),
                            "shares": 0.0,
                            "fund_name": fund_name
                        })
                        i += 2
                        continue
                i += 1

        return results

    def _is_fund_name(self, text: str, type_kws: List[str], suffixes: List[str],
                      company_prefixes: List[str]) -> bool:
        """判断文本是否是基金名称"""
        if not text or len(text) < 4 or len(text) > 35:
            return False

        # 必须包含基金类型关键词
        has_type = any(kw in text for kw in type_kws)
        if not has_type:
            return False

        # 以基金公司名开头直接通过
        has_company = any(text.startswith(cp) for cp in company_prefixes)
        if has_company:
            return True

        # 统计中文字符数量
        chinese_count = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')

        # 中文字符足够多也可以（放宽条件）
        if chinese_count >= 3 and len(text) >= 5:
            return True

        return False

    def _find_amounts_in_lines(self, lines: List[str]) -> List[Decimal]:
        """从文本行中提取金额"""
        amounts = []
        for line in lines:
            line = line.strip()
            # 跳过涨跌金额和百分比
            if line.startswith('+') or line.startswith('-') or '%' in line:
                continue
            # 跳过非数字内容
            if not line or not line[0].isdigit():
                continue
            try:
                clean = line.replace(',', '')
                # 金额格式：纯数字或带小数点
                if re.match(r'^\d+\.?\d*$', clean):
                    value = Decimal(clean)
                    if 10 < value < 10000000:  # 合理的持仓金额范围
                        amounts.append(value)
            except:
                pass
        return amounts

    def _validate_fund_data(self, data: Dict) -> bool:
        """验证基金数据合理性"""
        fund_code = data.get("fund_code", "")
        fund_name = data.get("fund_name", "")

        # 必须有基金代码或基金名称
        if not fund_code and not fund_name:
            return False

        # 如果有基金代码，检查格式
        if fund_code and not re.match(r'^\d{6}$', fund_code):
            return False

        # 检查金额
        amount = data.get("amount", 0)
        if amount <= 0:
            return False

        # 金额应该在合理范围内（0.01 到 1亿）
        if amount < 0.01 or amount > 100000000:
            return False

        return True

    async def recognize_from_base64(self, base64_data: str) -> List[Dict]:
        """从base64图片识别基金信息"""
        # 解码base64
        if ',' in base64_data:
            base64_data = base64_data.split(',')[1]

        image_data = base64.b64decode(base64_data)
        image = Image.open(io.BytesIO(image_data))
        image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        return await self.recognize_from_image(image_np)

    async def recognize_from_file(self, file_path: str) -> List[Dict]:
        """从文件识别基金信息"""
        image = cv2.imread(file_path)
        if image is None:
            raise ValueError("无法读取图片文件")

        return await self.recognize_from_image(image)

    def _extract_text_from_result(self, result) -> List[str]:
        """从OCR结果中提取文本，兼容不同版本的PaddleOCR"""
        text_lines = []

        if not result:
            return text_lines

        try:
            for item in result:
                if item is None:
                    continue

                # PaddleX OCRResult 对象（类字典）
                if hasattr(item, 'keys'):
                    for key in ['rec_texts', 'rec_text', 'texts', 'text']:
                        if key in item:
                            val = item[key]
                            if isinstance(val, list):
                                for t in val:
                                    if isinstance(t, str):
                                        text_lines.append(t)
                                    elif isinstance(t, (list, tuple)) and len(t) > 0:
                                        text_lines.append(str(t[0]))
                            elif isinstance(val, str):
                                text_lines.append(val)
                            break

                # 旧版格式
                elif isinstance(item, (list, tuple)):
                    for line in item:
                        if isinstance(line, (list, tuple)) and len(line) >= 2:
                            text_info = line[-1]
                            if isinstance(text_info, (list, tuple)) and len(text_info) >= 1:
                                text_lines.append(str(text_info[0]))
                            elif isinstance(text_info, str):
                                text_lines.append(text_info)
        except Exception as e:
            print(f"提取文本失败: {e}")

        return text_lines

    async def recognize_from_image(self, image: np.ndarray, enrich_info: bool = True) -> List[Dict]:
        """从图片数组识别基金信息

        Args:
            image: 图片数组
            enrich_info: 是否通过API搜索补充完整的基金代码和名称
        """
        ocr = self._get_ocr()

        # 对长图进行分段处理
        image_segments = self._split_long_image(image)

        all_text_lines = []

        # 对每个分段进行OCR
        for segment in image_segments:
            try:
                result = ocr.ocr(segment)
                text_lines = self._extract_text_from_result(result)
                all_text_lines.extend(text_lines)
            except Exception as e:
                print(f"OCR识别失败: {e}")
                continue

        # 从所有文本中提取基金信息
        all_results = self._extract_fund_info(all_text_lines)

        # 去重（基于fund_code或fund_name）
        unique_results = {}
        for item in all_results:
            if self._validate_fund_data(item):
                key = item["fund_code"] if item["fund_code"] else item["fund_name"]
                if key and key not in unique_results:
                    unique_results[key] = item

        results = list(unique_results.values())
        print(f"OCR识别到 {len(results)} 只基金")

        # 通过API搜索补充完整信息
        if enrich_info and results:
            results = await self._enrich_fund_info(results)

        return results

    def _clean_fund_name(self, name: str) -> str:
        """清理基金名称，去除不完整的后缀"""
        if not name:
            return name

        # 移除不完整的括号
        if '（' in name and '）' not in name:
            name = name.split('（')[0]
        if '(' in name and ')' not in name:
            name = name.split('(')[0]

        # 移除末尾的省略号或不完整字符
        name = name.rstrip('.。…')

        return name.strip()

    async def _enrich_fund_info(self, funds: List[Dict]) -> List[Dict]:
        """通过API搜索补充完整的基金代码和名称"""
        from .fund_service import fund_service

        enriched = []
        for fund in funds:
            fund_code = fund.get("fund_code", "")
            fund_name = fund.get("fund_name", "")
            amount = fund.get("amount", 0)

            # 如果已有基金代码，通过代码获取完整名称
            if fund_code:
                try:
                    fund_data = await fund_service.get_fund_realtime(fund_code)
                    if fund_data:
                        enriched.append({
                            "fund_code": fund_code,
                            "fund_name": fund_data.get("fund_name", fund_name),
                            "amount": amount,
                            "shares": fund.get("shares", 0.0)
                        })
                        continue
                except:
                    pass

            # 如果只有名称，通过名称搜索获取代码
            if fund_name:
                # 清理不完整的名称
                clean_name = self._clean_fund_name(fund_name)
                try:
                    search_result = await fund_service.search_fund_by_name(clean_name)
                    if search_result:
                        enriched.append({
                            "fund_code": search_result.get("fund_code", ""),
                            "fund_name": search_result.get("fund_name", fund_name),
                            "amount": amount,
                            "shares": fund.get("shares", 0.0)
                        })
                        print(f"搜索匹配: {fund_name} -> {search_result.get('fund_name')} ({search_result.get('fund_code')})")
                        continue
                except Exception as e:
                    print(f"搜索基金失败: {e}")

            # 搜索失败，保留原始数据
            enriched.append(fund)

        print(f"补充信息后共 {len(enriched)} 只基金")
        return enriched


# 全局实例
ocr_service = OCRService()
