from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base
from .api import portfolios, holdings, stats, ocr

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(portfolios.router)
app.include_router(holdings.router)
app.include_router(stats.router)
app.include_router(ocr.router)


@app.get("/")
def root():
    return {"message": "基金估值系统 API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok"}
