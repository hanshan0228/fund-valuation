# 快速启动指南

## 一键安装

```bash
chmod +x setup.sh
./setup.sh
```

## 手动安装

### 1. 后端安装

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 前端安装

```bash
cd frontend
npm install
```

## 启动服务

### 启动后端（终端1）

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python run.py
```

后端服务启动在: http://localhost:8000

### 启动前端（终端2）

```bash
cd frontend
npm run dev
```

前端服务启动在: http://localhost:5173

## 首次使用

1. 打开浏览器访问: http://localhost:5173

2. 创建第一个组合:
   - 点击"创建组合"
   - 输入组合名称（如：我的基金组合）
   - 点击确定

3. 添加持仓（两种方式）:

   **方式1: OCR识别（推荐）**
   - 打开支付宝，进入基金持仓页面
   - 截图保存
   - 点击"OCR上传"菜单
   - 上传截图
   - 确认识别结果
   - 选择组合，点击"导入到组合"

   **方式2: 手动添加**
   - 点击组合详情
   - 点击"添加持仓"
   - 输入基金代码、金额、份额
   - 点击确定

4. 查看实时收益:
   - 点击组合名称进入详情页
   - 系统自动获取实时估值
   - 交易时间每5分钟自动刷新

## 验证安装

### 检查后端

访问: http://localhost:8000/docs

应该能看到API文档页面

### 检查前端

访问: http://localhost:5173

应该能看到"基金估值系统"主页

## 常见安装问题

### Python依赖安装失败

如果遇到PaddleOCR安装失败:

```bash
# 尝试单独安装
pip install paddlepaddle
pip install paddleocr
```

### npm安装慢

使用国内镜像:

```bash
npm config set registry https://registry.npmmirror.com
npm install
```

### 端口被占用

修改端口:

**后端** - 编辑 `backend/run.py`:
```python
uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
```

**前端** - 编辑 `frontend/vite.config.js`:
```javascript
server: {
  port: 5174
}
```

## 生产部署

### 后端

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 前端

```bash
cd frontend
npm run build
# 将 dist 目录部署到nginx或其他Web服务器
```

## 技术支持

如遇到问题，请查看:

1. 完整文档: README.md
2. API文档: http://localhost:8000/docs
3. 浏览器控制台错误信息
4. 后端终端错误信息

## 下一步

- 查看 README.md 了解完整功能
- 尝试使用OCR识别功能
- 查看历史收益统计图表
- 探索API文档，进行二次开发
