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
            from paddleocr import PaddleOCR
            self._ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=False, show_log=False)
        return self._ocr

    def _preprocess_image(self, image: np.ndarray) -> List[np.ndarray]:
        """图片预处理，返回多个策略的图片"""
        images = []

        # 策略1: 原图
        images.append(image)

        # 策略2: 灰度化
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        images.append(gray)

        # 策略3: 二值化
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        images.append(binary)

        # 策略4: 增强对比度
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        images.append(enhanced)

        return images

    def _extract_fund_info(self, text_lines: List[str]) -> List[Dict]:
        """从OCR文本中提取基金信息"""
        results = []

        # 正则模式
        fund_code_pattern = re.compile(r'\b(\d{6})\b')
        amount_pattern = re.compile(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)')

        i = 0
        while i < len(text_lines):
            line = text_lines[i]

            # 查找基金代码
            code_match = fund_code_pattern.search(line)
            if code_match:
                fund_code = code_match.group(1)

                # 在当前行和后续几行查找金额和份额
                search_lines = text_lines[i:min(i+5, len(text_lines))]
                amounts = []

                for search_line in search_lines:
                    # 提取所有数字
                    amount_matches = amount_pattern.findall(search_line)
                    for amt in amount_matches:
                        # 移除逗号并转换
                        try:
                            value = Decimal(amt.replace(',', ''))
                            if value > 0:
                                amounts.append(value)
                        except:
                            pass

                # 尝试识别金额和份额
                # 支付宝截图通常显示：持仓金额 和 持有份额
                if len(amounts) >= 2:
                    # 假设较大的是金额，较小的是份额（但不绝对）
                    # 更安全的做法是让用户确认
                    amount = amounts[0]
                    shares = amounts[1] if len(amounts) > 1 else amounts[0]

                    results.append({
                        "fund_code": fund_code,
                        "amount": float(amount),
                        "shares": float(shares),
                        "fund_name": ""  # 需要从API获取
                    })

                i += 5  # 跳过已处理的行
            else:
                i += 1

        return results

    def _validate_fund_data(self, data: Dict) -> bool:
        """验证基金数据合理性"""
        # 检查代码格式
        if not re.match(r'^\d{6}$', data.get("fund_code", "")):
            return False

        # 检查金额和份额
        amount = data.get("amount", 0)
        shares = data.get("shares", 0)

        if amount <= 0 or shares <= 0:
            return False

        # 检查金额份额比例合理性（净值一般在0.5-10之间）
        nav = amount / shares
        if nav < 0.1 or nav > 100:
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

    async def recognize_from_image(self, image: np.ndarray) -> List[Dict]:
        """从图片数组识别基金信息"""
        ocr = self._get_ocr()

        # 预处理得到多个策略的图片
        processed_images = self._preprocess_image(image)

        all_results = []

        # 对每个策略进行OCR
        for proc_img in processed_images:
            try:
                result = ocr.ocr(proc_img, cls=True)

                if result and result[0]:
                    # 提取文本
                    text_lines = [line[1][0] for line in result[0]]

                    # 提取基金信息
                    fund_infos = self._extract_fund_info(text_lines)

                    all_results.extend(fund_infos)
            except Exception as e:
                print(f"OCR识别失败: {e}")
                continue

        # 去重（基于fund_code）
        unique_results = {}
        for item in all_results:
            if self._validate_fund_data(item):
                code = item["fund_code"]
                if code not in unique_results:
                    unique_results[code] = item

        return list(unique_results.values())


# 全局实例
ocr_service = OCRService()
