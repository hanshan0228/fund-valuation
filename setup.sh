#!/bin/bash

echo "========================================="
echo "基金实时估值系统 - 安装脚本"
echo "========================================="

# 创建数据目录
echo ""
echo "创建数据目录..."
mkdir -p data/uploads data/logs

# 后端安装
echo ""
echo "========================================="
echo "安装后端依赖..."
echo "========================================="
cd backend

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
echo "检测到Python版本: $python_version"

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装Python依赖包..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "后端安装完成!"

# 前端安装
cd ../frontend
echo ""
echo "========================================="
echo "安装前端依赖..."
echo "========================================="

# 检查npm
if ! command -v npm &> /dev/null; then
    echo "错误: 未检测到npm，请先安装Node.js"
    exit 1
fi

npm_version=$(npm --version)
echo "检测到npm版本: $npm_version"

echo "安装前端依赖包..."
npm install

echo ""
echo "前端安装完成!"

# 完成
cd ..
echo ""
echo "========================================="
echo "安装完成!"
echo "========================================="
echo ""
echo "启动说明："
echo ""
echo "1. 启动后端服务:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python run.py"
echo ""
echo "2. 启动前端服务（新终端）:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. 访问应用:"
echo "   http://localhost:5173"
echo ""
echo "========================================="
