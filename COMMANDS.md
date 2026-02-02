# 常用命令速查

## 🚀 安装和启动

### 一键安装
```bash
chmod +x setup.sh
./setup.sh
```

### 后端安装
```bash
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境 (macOS/Linux)
source venv/bin/activate

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 测试安装
python test_install.py
```

### 前端安装
```bash
cd frontend

# 安装依赖
npm install

# 或使用国内镜像
npm config set registry https://registry.npmmirror.com
npm install
```

## 🏃 运行应用

### 后端开发服务器
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python run.py
```

### 前端开发服务器
```bash
cd frontend
npm run dev
```

### 生产环境

**后端**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**前端**
```bash
cd frontend
npm run build
# 将 dist/ 目录部署到 Web 服务器
```

## 🧪 测试

### 后端测试
```bash
cd backend
source venv/bin/activate

# 运行安装测试
python test_install.py

# 安装pytest (如需单元测试)
pip install pytest pytest-asyncio

# 运行测试
pytest
```

### 前端测试
```bash
cd frontend

# 安装测试依赖
npm install -D vitest @vue/test-utils

# 运行测试
npm run test
```

## 🔍 调试

### 查看API文档
```bash
# 启动后端后访问
http://localhost:8000/docs        # Swagger UI
http://localhost:8000/redoc       # ReDoc
http://localhost:8000/health      # 健康检查
```

### Python调试
```python
# 添加断点
import pdb; pdb.set_trace()

# 查看变量
print(f"Debug: {variable}")
```

### Vue调试
```javascript
// 控制台输出
console.log('Debug:', data)

// 使用Vue DevTools
# 安装Chrome扩展: Vue.js devtools
```

## 📦 依赖管理

### 后端更新依赖
```bash
cd backend
source venv/bin/activate

# 更新单个包
pip install --upgrade fastapi

# 更新所有包
pip install --upgrade -r requirements.txt

# 冻结依赖版本
pip freeze > requirements.txt
```

### 前端更新依赖
```bash
cd frontend

# 查看过期包
npm outdated

# 更新单个包
npm update vue

# 更新所有包
npm update

# 安装新包
npm install <package-name>
```

## 🗄️ 数据库操作

### 查看数据库
```bash
# 安装sqlite3
brew install sqlite3  # macOS
apt-get install sqlite3  # Linux

# 打开数据库
sqlite3 data/database.db

# 查看所有表
.tables

# 查看表结构
.schema portfolios

# 查询数据
SELECT * FROM portfolios;

# 退出
.quit
```

### 重置数据库
```bash
# 删除数据库文件
rm data/database.db

# 重新启动后端，会自动创建
python run.py
```

## 🔧 配置修改

### 修改后端端口
编辑 `backend/run.py`:
```python
uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
```

### 修改前端端口
编辑 `frontend/vite.config.js`:
```javascript
server: {
  port: 5174
}
```

### 修改缓存时间
编辑 `backend/.env`:
```env
FUND_CACHE_TTL=600  # 10分钟
```

## 📝 日志查看

### 后端日志
```bash
# 终端实时输出
python run.py

# 如有文件日志
tail -f data/logs/app.log
```

### 前端日志
```bash
# 浏览器开发者工具
# F12 -> Console
```

## 🧹 清理

### 清理Python缓存
```bash
cd backend
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### 清理前端构建
```bash
cd frontend
rm -rf dist/
rm -rf node_modules/
npm install
```

### 完全重置
```bash
# 删除所有生成文件
rm -rf backend/venv/
rm -rf backend/__pycache__/
rm -rf frontend/node_modules/
rm -rf frontend/dist/
rm -rf data/database.db

# 重新安装
./setup.sh
```

## 📊 性能分析

### 后端性能
```bash
# 安装分析工具
pip install py-spy

# 分析运行中的应用
py-spy top --pid <PID>
```

### 前端性能
```bash
# 构建分析
npm run build -- --report

# 使用Lighthouse (Chrome DevTools)
# F12 -> Lighthouse -> 生成报告
```

## 🔐 安全检查

### Python安全扫描
```bash
pip install safety
safety check
```

### npm安全审计
```bash
npm audit
npm audit fix
```

## 🐳 Docker (可选)

### 创建Dockerfile
```bash
# 后端 Dockerfile
cd backend
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# 构建镜像
docker build -t fund-backend .

# 运行容器
docker run -p 8000:8000 fund-backend
```

## 📱 快捷操作

### 快速重启
```bash
# 后端
cd backend && source venv/bin/activate && python run.py

# 前端
cd frontend && npm run dev
```

### 查看项目结构
```bash
# 使用find
find . -type f -name "*.py" | head -20

# 使用tree (需安装)
tree -L 3 -I 'node_modules|venv|__pycache__'
```

### 统计代码行数
```bash
# Python代码
find backend -name "*.py" | xargs wc -l

# Vue代码
find frontend/src -name "*.vue" | xargs wc -l

# 所有代码
find . -name "*.py" -o -name "*.vue" -o -name "*.js" | grep -v node_modules | grep -v venv | xargs wc -l
```

## 🆘 故障排除

### 端口被占用
```bash
# 查找占用端口的进程
lsof -i :8000  # 后端
lsof -i :5173  # 前端

# 杀死进程
kill -9 <PID>
```

### 依赖安装失败
```bash
# Python
pip install --upgrade pip
pip cache purge
pip install -r requirements.txt

# npm
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### 数据库锁定
```bash
# 关闭所有访问数据库的进程
# 删除锁文件
rm data/database.db-journal
```

## 📚 更多帮助

查看完整文档:
- `README.md` - 项目说明
- `QUICKSTART.md` - 快速开始
- `DEVELOPMENT.md` - 开发指南
