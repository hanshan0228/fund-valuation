# 开发指南

## 目录结构详解

```
fund-valuation/
├── backend/                      # 后端代码
│   ├── app/
│   │   ├── api/                 # API路由层
│   │   │   ├── portfolios.py    # 组合管理API
│   │   │   ├── holdings.py      # 持仓管理API
│   │   │   ├── stats.py         # 统计数据API
│   │   │   └── ocr.py           # OCR识别API
│   │   ├── models/              # 数据模型（SQLAlchemy）
│   │   │   ├── portfolio.py     # 组合模型
│   │   │   ├── holding.py       # 持仓模型
│   │   │   ├── fund.py          # 基金信息模型
│   │   │   └── history.py       # 历史记录模型
│   │   ├── schemas/             # 数据验证（Pydantic）
│   │   │   ├── portfolio.py
│   │   │   ├── holding.py
│   │   │   ├── fund.py
│   │   │   └── stats.py
│   │   ├── services/            # 业务逻辑层
│   │   │   ├── fund_service.py  # 基金数据服务
│   │   │   ├── ocr_service.py   # OCR识别服务
│   │   │   └── stats_service.py # 统计计算服务
│   │   ├── tasks/               # 定时任务（未实现）
│   │   ├── utils/               # 工具函数
│   │   ├── config.py            # 配置管理
│   │   ├── database.py          # 数据库连接
│   │   └── main.py              # FastAPI应用入口
│   ├── requirements.txt         # Python依赖
│   ├── run.py                   # 开发服务器启动
│   └── test_install.py          # 安装测试脚本
├── frontend/                     # 前端代码
│   ├── src/
│   │   ├── api/                 # API调用封装
│   │   │   └── index.js
│   │   ├── views/               # 页面组件
│   │   │   ├── PortfolioList.vue    # 组合列表
│   │   │   ├── PortfolioDetail.vue  # 组合详情
│   │   │   ├── UploadOCR.vue        # OCR上传
│   │   │   └── Statistics.vue       # 统计图表
│   │   ├── stores/              # 状态管理（Pinia）
│   │   │   └── portfolio.js
│   │   ├── router/              # 路由配置
│   │   │   └── index.js
│   │   ├── App.vue              # 根组件
│   │   └── main.js              # 应用入口
│   ├── package.json             # npm依赖
│   └── vite.config.js           # Vite配置
├── data/                         # 数据目录
│   ├── database.db              # SQLite数据库
│   ├── uploads/                 # 上传文件
│   └── logs/                    # 日志文件
└── README.md                    # 项目说明
```

## 添加新功能

### 1. 添加新的API端点

#### 后端步骤

**1.1 创建Schema（如需要）**

`backend/app/schemas/your_feature.py`:
```python
from pydantic import BaseModel

class YourFeatureCreate(BaseModel):
    name: str
    value: int

class YourFeatureResponse(BaseModel):
    id: int
    name: str
    value: int

    model_config = ConfigDict(from_attributes=True)
```

**1.2 创建API路由**

`backend/app/api/your_feature.py`:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/api/your-feature", tags=["your-feature"])

@router.get("")
def get_items(db: Session = Depends(get_db)):
    return {"message": "Your feature"}
```

**1.3 注册路由**

在 `backend/app/main.py` 中:
```python
from .api import your_feature

app.include_router(your_feature.router)
```

#### 前端步骤

**1.1 添加API调用**

在 `frontend/src/api/index.js` 中:
```javascript
export const yourFeatureAPI = {
  getAll: () => api.get('/your-feature'),
  create: (data) => api.post('/your-feature', data)
}
```

**1.2 创建页面组件**

`frontend/src/views/YourFeature.vue`:
```vue
<template>
  <div>
    <h1>Your Feature</h1>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { yourFeatureAPI } from '../api'

const items = ref([])

const loadItems = async () => {
  items.value = await yourFeatureAPI.getAll()
}

onMounted(() => {
  loadItems()
})
</script>
```

**1.3 添加路由**

在 `frontend/src/router/index.js` 中:
```javascript
{
  path: '/your-feature',
  name: 'YourFeature',
  component: () => import('../views/YourFeature.vue')
}
```

### 2. 添加新的数据模型

**2.1 创建模型**

`backend/app/models/your_model.py`:
```python
from sqlalchemy import Column, Integer, String
from ..database import Base

class YourModel(Base):
    __tablename__ = "your_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
```

**2.2 导入模型**

在 `backend/app/models/__init__.py` 中:
```python
from .your_model import YourModel

__all__ = [..., "YourModel"]
```

**2.3 创建数据库表**

重启应用，SQLAlchemy会自动创建表。或手动执行:
```python
from app.database import engine, Base
Base.metadata.create_all(bind=engine)
```

## 调试技巧

### 后端调试

**1. 启用详细日志**

在 `backend/.env` 中:
```
DEBUG=True
```

**2. 使用print调试**

```python
print(f"Debug: {variable}")
```

**3. 使用pdb断点**

```python
import pdb; pdb.set_trace()
```

**4. 查看API文档**

访问: http://localhost:8000/docs

### 前端调试

**1. 浏览器开发者工具**

- F12 打开开发者工具
- Console - 查看日志
- Network - 查看API请求

**2. Vue DevTools**

安装Chrome扩展: Vue.js devtools

**3. 添加console.log**

```javascript
console.log('Debug:', data)
```

## 性能优化

### 后端优化

**1. 数据库查询优化**

使用索引:
```python
class YourModel(Base):
    __tablename__ = "your_table"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), index=True)  # 添加索引
```

**2. 批量查询**

避免N+1问题:
```python
# 不好
for item in items:
    fund = db.query(Fund).filter(Fund.code == item.code).first()

# 好
codes = [item.code for item in items]
funds = db.query(Fund).filter(Fund.code.in_(codes)).all()
```

**3. 缓存策略**

已实现在 `fund_service.py` 中。

### 前端优化

**1. 懒加载路由**

已实现:
```javascript
component: () => import('../views/YourView.vue')
```

**2. 防抖和节流**

```javascript
import { debounce } from 'lodash-es'

const search = debounce(async (keyword) => {
  // 搜索逻辑
}, 300)
```

**3. 虚拟滚动**

对于大列表，使用 `el-virtual-list`。

## 测试

### 后端测试

**安装pytest**

```bash
pip install pytest pytest-asyncio
```

**创建测试文件**

`backend/tests/test_fund_service.py`:
```python
import pytest
from app.services.fund_service import fund_service

@pytest.mark.asyncio
async def test_get_fund_realtime():
    result = await fund_service.get_fund_realtime("001632")
    assert result is not None
    assert result["fund_code"] == "001632"
```

**运行测试**

```bash
pytest
```

### 前端测试

**安装Vitest**

```bash
npm install -D vitest @vue/test-utils
```

**创建测试文件**

`frontend/src/components/__tests__/YourComponent.spec.js`:
```javascript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import YourComponent from '../YourComponent.vue'

describe('YourComponent', () => {
  it('renders properly', () => {
    const wrapper = mount(YourComponent)
    expect(wrapper.text()).toContain('Expected Text')
  })
})
```

## 常见问题

### Q: 如何修改端口？

**后端**: 修改 `backend/run.py`:
```python
uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
```

**前端**: 修改 `frontend/vite.config.js`:
```javascript
server: {
  port: 5174
}
```

### Q: 如何添加新的基金数据源？

修改 `backend/app/services/fund_service.py`，在 `_fetch_from_api` 方法中添加备用API。

### Q: 如何修改缓存时间？

修改 `backend/.env`:
```
FUND_CACHE_TTL=600  # 10分钟
```

### Q: 如何添加用户认证？

1. 安装依赖: `pip install python-jose passlib`
2. 实现JWT认证中间件
3. 添加用户模型和登录API
4. 前端添加登录页面和token管理

## 贡献指南

1. Fork项目
2. 创建功能分支: `git checkout -b feature/your-feature`
3. 提交更改: `git commit -am 'Add your feature'`
4. 推送分支: `git push origin feature/your-feature`
5. 提交Pull Request

## 代码规范

### Python

遵循PEP 8:
```bash
pip install black flake8
black .
flake8 .
```

### JavaScript

使用ESLint和Prettier:
```bash
npm install -D eslint prettier
npm run lint
```

## 参考资源

- [FastAPI文档](https://fastapi.tiangolo.com/)
- [Vue 3文档](https://vuejs.org/)
- [Element Plus文档](https://element-plus.org/)
- [SQLAlchemy文档](https://docs.sqlalchemy.org/)
- [PaddleOCR文档](https://github.com/PaddlePaddle/PaddleOCR)
