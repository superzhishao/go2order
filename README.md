# YShop Drink - Python 版

基于 [yshop-drink](https://gitee.com/guchengwuyue/yshop-drink) 的 Python 复刻版本。

扫码点餐系统，支持在线点餐（外卖与自取）、多门店模式。

## 技术栈

| 原版 (Java) | Python 版 |
|---|---|
| Spring Boot 3 | FastAPI |
| MyBatis Plus | SQLAlchemy 2.0 (async) |
| Spring Security OAuth2 | JWT (python-jose) |
| MySQL | PostgreSQL |
| Redis | Redis (aioredis) |
| Maven | pip |

## 功能模块

- **会员认证** - 手机号登录、短信验证码登录、微信小程序登录、JWT Token
- **门店管理** - 多门店、营业状态、地理位置、配送范围
- **商品管理** - 分类、商品(多规格SKU)、上下架
- **订单管理** - 自取/外卖、取餐号、订单状态流转、退款
- **优惠券** - 创建、领取、使用、过期管理
- **积分系统** - 积分商品、积分兑换
- **管理后台** - 商品/订单/门店/会员/优惠券/积分 CRUD

## 项目结构

```
app/
├── main.py              # FastAPI 入口
├── config.py            # 配置
├── database.py          # 数据库连接
├── deps.py              # 依赖注入 (认证等)
├── models/              # SQLAlchemy 模型
│   ├── user.py          # 会员、地址、账单
│   ├── product.py       # 商品、分类、SKU
│   ├── order.py         # 订单、订单详情
│   ├── store.py         # 门店
│   ├── coupon.py        # 优惠券
│   ├── score.py         # 积分商品/订单
│   └── system.py        # 系统用户、角色、菜单
├── schemas/             # Pydantic 请求/响应模型
├── services/            # 业务逻辑层
├── api/
│   ├── app/             # 移动端/H5 API (/app-api)
│   └── admin/           # 管理后台 API (/admin-api)
└── utils/               # 工具函数
```

## 快速启动

### 方式一：Docker Compose（推荐）

```bash
docker-compose up -d
```

服务启动后：
- API: http://localhost:8080
- API 文档: http://localhost:8080/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### 方式二：本地开发

#### 1. 环境要求

- Python 3.11+
- PostgreSQL 14+
- Redis 6+

#### 2. 安装依赖

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 配置数据库和 Redis 连接
```

#### 4. 创建数据库

```bash
createdb yshop_drink
```

#### 5. 运行数据库迁移

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

#### 6. 创建管理员账号

```python
# 使用 Python shell
from app.utils.security import hash_password
print(hash_password("admin123"))
# 将密码哈希插入 system_users 表
```

#### 7. 启动服务

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## API 文档

启动后访问:
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

### 主要 API 路径

| 模块 | 移动端 | 管理后台 |
|---|---|---|
| 认证 | `/app-api/member/auth/*` | `/admin-api/system/auth/*` |
| 商品 | `/app-api/product/*` | `/admin-api/product/*` |
| 订单 | `/app-api/order/*` | `/admin-api/order/*` |
| 门店 | `/app-api/store/*` | `/admin-api/store/*` |
| 优惠券 | `/app-api/coupon/*` | `/admin-api/coupon/*` |
| 积分 | `/app-api/score/*` | `/admin-api/score/*` |
| 用户 | `/app-api/user/*` | `/admin-api/member/user/*` |

## 前端对接

本项目后端 API 设计兼容原版 yshop-drink 的前端：
- **管理后台**: yshop-drink-vue3 (Vue3 + Element Plus)
- **移动端**: yshop-drink-uniapp-vue3 (UniApp Vue3)

只需修改前端 `.env` 中的 API 地址即可对接。

## 开源协议

MIT License
