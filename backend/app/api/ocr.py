from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import cv2
import numpy as np
from ..services.ocr_service import ocr_service

router = APIRouter(prefix="/api/ocr", tags=["ocr"])


class OCRBase64Request(BaseModel):
    image: str


@router.post("/upload")
async def upload_ocr(file: UploadFile = File(...)):
    """上传图片进行OCR识别"""
    try:
        # 读取文件
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            raise HTTPException(status_code=400, detail="无法读取图片")

        # OCR识别
        results = await ocr_service.recognize_from_image(image)

        return {
            "success": True,
            "count": len(results),
            "data": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR识别失败: {str(e)}")


@router.post("/upload-base64")
async def upload_ocr_base64(request: OCRBase64Request):
    """上传base64图片进行OCR识别"""
    try:
        results = await ocr_service.recognize_from_base64(request.image)

        return {
            "success": True,
            "count": len(results),
            "data": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR识别失败: {str(e)}")
