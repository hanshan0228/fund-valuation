#!/usr/bin/env python
"""
测试脚本 - 验证依赖是否正确安装
"""

import sys

def test_imports():
    """测试所有依赖包是否可以导入"""
    print("测试依赖包导入...")

    packages = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'sqlalchemy': 'SQLAlchemy',
        'aiohttp': 'aiohttp',
        'paddleocr': 'PaddleOCR',
        'cv2': 'OpenCV',
        'PIL': 'Pillow',
        'apscheduler': 'APScheduler',
        'pydantic': 'Pydantic',
    }

    failed = []

    for module, name in packages.items():
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError as e:
            print(f"✗ {name}: {e}")
            failed.append(name)

    if failed:
        print(f"\n失败: {len(failed)} 个包导入失败")
        print(f"失败的包: {', '.join(failed)}")
        return False
    else:
        print(f"\n成功: 所有依赖包导入正常")
        return True

def test_database():
    """测试数据库连接"""
    print("\n测试数据库...")

    try:
        from app.database import engine, Base
        from app.models import Portfolio, Holding, Fund, History

        # 创建表
        Base.metadata.create_all(bind=engine)
        print("✓ 数据库表创建成功")

        return True
    except Exception as e:
        print(f"✗ 数据库测试失败: {e}")
        return False

def test_ocr():
    """测试OCR功能"""
    print("\n测试OCR...")

    try:
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=False, show_log=False)
        print("✓ PaddleOCR初始化成功")
        return True
    except Exception as e:
        print(f"✗ OCR测试失败: {e}")
        return False

def main():
    print("=" * 50)
    print("基金估值系统 - 安装测试")
    print("=" * 50)
    print(f"Python版本: {sys.version}")
    print("=" * 50)

    results = []

    # 测试导入
    results.append(test_imports())

    # 测试数据库
    results.append(test_database())

    # 测试OCR
    results.append(test_ocr())

    # 总结
    print("\n" + "=" * 50)
    if all(results):
        print("✓ 所有测试通过! 可以启动应用了")
        print("\n启动命令:")
        print("  python run.py")
    else:
        print("✗ 部分测试失败，请检查依赖安装")
        print("\n请运行:")
        print("  pip install -r requirements.txt")
    print("=" * 50)

if __name__ == "__main__":
    main()
