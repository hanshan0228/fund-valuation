# 基金实时估值系统

一个基于 FastAPI + Vue 3 的基金估值系统，支持OCR识别支付宝基金持仓截图、实时估值更新、历史收益统计和多组合管理。

## 功能特性

- ✅ **OCR识别**: 上传支付宝基金持仓截图，自动识别基金代码、金额和份额
- ✅ **实时估值**: 从天天基金网获取实时估值，交易时间自动刷新
- ✅ **多组合管理**: 支持创建多个基金组合，独立管理
- ✅ **收益统计**: 实时计算收益和收益率，查看历史收益曲线
- ✅ **数据私密**: 本地运行，数据存储在本地SQLite数据库

## 技术栈

### 后端
- FastAPI - 高性能异步Web框架
- SQLAlchemy - ORM框架
- SQLite - 轻量级数据库
- PaddleOCR - OCR识别引擎
- aiohttp - 异步HTTP客户端

### 前端
- Vue 3 - 渐进式JavaScript框架
- Element Plus - UI组件库
- Pinia - 状态管理
- ECharts - 数据可视化
- Axios - HTTP客户端

## 项目结构

```
fund-valuation/
├── backend/                # 后端代码
│   ├── app/
│   │   ├── api/           # API路由
│   │   ├── models/        # 数据模型
│   │   ├── schemas/       # Pydantic模型
│   │   ├── services/      # 业务逻辑
│   │   ├── config.py      # 配置
│   │   └── main.py        # 应用入口
│   ├── requirements.txt   # Python依赖
│   └── run.py            # 启动脚本
├── frontend/              # 前端代码
│   ├── src/
│   │   ├── api/          # API调用
│   │   ├── views/        # 页面组件
│   │   ├── stores/       # Pinia stores
│   │   └── router/       # 路由配置
│   └── package.json      # npm依赖
├── data/                  # 数据目录
│   ├── database.db       # SQLite数据库
│   ├── uploads/          # 上传文件
│   └── logs/             # 日志文件
└── README.md
```

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 后端安装

```bash
# 进入后端目录
cd fund-valuation/backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动后端服务
python run.py
```

后端服务将运行在 http://localhost:8000

### 前端安装

```bash
# 进入前端目录
cd fund-valuation/frontend

# 安装依赖
npm install

# 启动前端开发服务器
npm run dev
```

前端服务将运行在 http://localhost:5173

## 使用指南

### 1. 创建组合

1. 访问 http://localhost:5173
2. 点击"创建组合"按钮
3. 输入组合名称和描述
4. 点击确定

### 2. OCR识别导入持仓

1. 在支付宝中打开基金持仓页面，截图保存
2. 点击"OCR上传"菜单
3. 上传截图文件
4. 系统自动识别基金代码、金额、份额
5. 确认识别结果，可手动编辑修正
6. 选择目标组合，点击"导入到组合"

### 3. 查看实时收益

1. 在组合列表中点击"查看详情"
2. 系统自动从天天基金网获取实时估值
3. 显示每只基金的当前净值、收益和收益率
4. 交易时间（9:30-15:00）每5分钟自动刷新
5. 可手动点击"刷新"按钮立即更新

### 4. 查看历史统计

1. 点击"收益统计"菜单
2. 选择组合和时间范围
3. 查看收益曲线图

## API文档

启动后端后，访问以下地址查看自动生成的API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 核心API接口

### 组合管理

- `GET /api/portfolios` - 获取所有组合
- `POST /api/portfolios` - 创建组合
- `GET /api/portfolios/{id}` - 获取组合详情
- `PUT /api/portfolios/{id}` - 更新组合
- `DELETE /api/portfolios/{id}` - 删除组合

### 持仓管理

- `GET /api/portfolios/{id}/holdings` - 获取持仓列表
- `POST /api/portfolios/{id}/holdings` - 添加持仓
- `POST /api/portfolios/{id}/holdings/batch` - 批量导入
- `PUT /api/holdings/{id}` - 更新持仓
- `DELETE /api/holdings/{id}` - 删除持仓

### 收益统计

- `GET /api/portfolios/{id}/realtime` - 获取实时收益
- `GET /api/portfolios/{id}/history` - 获取历史收益

### OCR识别

- `POST /api/ocr/upload` - 上传图片识别
- `POST /api/ocr/upload-base64` - 上传base64图片识别

## 配置说明

后端配置文件: `backend/.env`

```env
# 应用配置
APP_NAME=基金估值系统
DEBUG=True

# 数据库
DATABASE_URL=sqlite:///./data/database.db

# OCR
OCR_USE_GPU=False
OCR_LANG=ch

# 基金API
FUND_API_TIMEOUT=10
FUND_CACHE_TTL=300
```

## 数据源

- **实时估值**: 天天基金网 (`http://fundgz.1234567.com.cn/js/{fund_code}.js`)
- 数据更新频率: 交易日 9:30-15:00，每5分钟更新一次

## 注意事项

1. **OCR准确性**: OCR识别结果可能存在误差，导入前请仔细核对
2. **数据时效性**: 估值数据来自第三方，可能存在延迟
3. **网络依赖**: 需要联网才能获取实时估值数据
4. **交易时间**: 非交易时间显示的是最近一次的估值数据
5. **首次启动**: 首次启动时需要下载PaddleOCR模型，可能需要一些时间

## 常见问题

### Q: OCR识别失败怎么办？
A:
1. 确保图片清晰，文字可辨识
2. 尝试调整图片亮度和对比度
3. 可以手动添加持仓，不依赖OCR

### Q: 实时估值不更新？
A:
1. 检查网络连接
2. 确认是否交易时间（9:30-15:00）
3. 手动点击刷新按钮
4. 查看浏览器控制台是否有错误

### Q: 如何备份数据？
A: 直接复制 `data/database.db` 文件即可

## 开发计划

- [ ] 支持更多数据源（东方财富、新浪财经）
- [ ] 添加定时任务，自动记录每日收益
- [ ] 支持导出数据为Excel
- [ ] 添加收益提醒功能
- [ ] 支持多设备同步

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 免责声明

本系统仅供学习和个人使用，不构成任何投资建议。投资有风险，入市需谨慎。
