# 🚀 启动指南

## ✅ 当前状态

- **后端服务**: ✅ 运行中 (http://localhost:8000)
- **前端服务**: ✅ 运行中 (http://localhost:5173)
- **数据库**: ✅ 已创建

## 🌐 访问方式

### 1. 打开浏览器直接访问

**前端界面**:
```
http://localhost:5173
```

**API文档**:
```
http://localhost:8000/docs
```

### 2. 使用命令行

```bash
# macOS
open http://localhost:5173

# Linux
xdg-open http://localhost:5173
```

## 📊 服务信息

### 后端 (FastAPI)
- 地址: http://localhost:8000
- 健康检查: http://localhost:8000/health
- API文档: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 日志: data/logs/backend.log

### 前端 (Vue 3 + Vite)
- 地址: http://localhost:5173
- 日志: data/logs/frontend.log

## 🎯 快速体验

1. **访问系统**
   ```
   打开浏览器访问: http://localhost:5173
   ```

2. **创建第一个组合**
   - 点击"创建组合"按钮
   - 输入组合名称（如：我的基金组合）
   - 点击确定

3. **手动添加持仓**（暂时跳过OCR）
   - 进入组合详情
   - 手动添加基金
   - 输入基金代码（如：001632）
   - 输入金额和份额
   - 查看实时收益

4. **查看API文档**
   ```
   访问: http://localhost:8000/docs
   ```

## 🔧 管理服务

### 查看运行状态
```bash
# 查看后端
curl http://localhost:8000/health

# 查看进程
ps aux | grep -E "(python run.py|vite)"
```

### 停止服务
```bash
# 进入项目目录
cd /Users/xzcabbage/workspace/code/cc/fund-valuation

# 停止所有服务
pkill -f "python run.py"
pkill -f "vite"
```

### 重启服务
```bash
# 后端
cd backend
source venv/bin/activate
nohup python run.py > ../data/logs/backend.log 2>&1 &

# 前端
cd frontend
nohup npm run dev > ../data/logs/frontend.log 2>&1 &
```

### 查看日志
```bash
# 后端日志
tail -f data/logs/backend.log

# 前端日志  
tail -f data/logs/frontend.log
```

## ⚠️ 故障排除

### 如果前端无法访问

1. 检查进程是否运行
   ```bash
   ps aux | grep vite
   ```

2. 查看日志
   ```bash
   tail -30 data/logs/frontend.log
   ```

3. 重启前端
   ```bash
   pkill -f vite
   cd frontend
   npm run dev
   ```

### 如果后端无法访问

1. 检查日志
   ```bash
   tail -30 data/logs/backend.log
   ```

2. 重启后端
   ```bash
   pkill -f "python run.py"
   cd backend
   source venv/bin/activate
   python run.py
   ```

## 💡 提示

- 首次启动可能需要下载PaddleOCR模型（约100MB）
- OCR功能需要上传清晰的支付宝截图
- 实时估值功能需要联网
- 交易时间（9:30-15:00）系统会自动刷新数据

## 📱 下一步

1. 打开浏览器访问 http://localhost:5173
2. 创建你的第一个基金组合
3. 尝试添加持仓
4. 查看实时收益

享受使用！🎉
