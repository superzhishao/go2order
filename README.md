# Go2Order

Scan-to-order restaurant system with multi-language and multi-currency support.

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy 2.0 (async) + MySQL 8.0
- **Frontend**: Single-file SPA (vanilla HTML/CSS/JS, no build tools)
- **Auth**: JWT (python-jose)
- **Cache**: Redis (aioredis)

## Features

- **11 Languages** — zh, en, de, fr, it, es, ja, ko, pt, hi, ar
- **Multi-currency** — configurable per shop (¥, $, €, £, etc.)
- **QR Table Ordering** — customers scan, select language, order from phone
- **Admin Panel** — products, orders, tables, coupons, settings
- **Multi-store** — multiple shops with independent settings
- **Product i18n** — name, description, info all support per-language translations
- **Round-based Orders** — group orders by table + time round for kitchen efficiency

## Quick Start

### 1. Install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env: set DATABASE_URL, REDIS_URL, SECRET_KEY
```

### 3. Seed database (first time)

The app auto-seeds on first startup if the database is empty. Or run manually:

```bash
python -m scripts.seed
```

This imports `scripts/init-db.sql` with full schema + demo data (shop, products, categories, tables, admin user).

### 4. Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

- **Customer H5**: http://localhost:8080/
- **Admin Panel**: http://localhost:8080/admin
- **API Docs**: http://localhost:8080/docs

Default admin login: `admin` / `admin123`

## Project Structure

```
app/
├── main.py              # FastAPI entry + auto-seed lifespan
├── config.py            # Settings (.env)
├── database.py          # SQLAlchemy async engine
├── models/              # ORM models
├── schemas/             # Pydantic request/response
├── services/            # Business logic
├── api/
│   ├── app/             # Customer H5 API (/app-api)
│   └── admin/           # Admin API (/admin-api)
└── utils/               # Helpers (response, security)

scripts/
├── init-db.sql          # Full schema + seed data
└── seed.py              # Auto-seed script

static/
├── h5/index.html        # Customer SPA
└── admin/index.html     # Admin SPA
```

## API Routes

| Module | Customer | Admin |
|--------|----------|-------|
| Auth | `/app-api/member/auth/*` | `/admin-api/system/auth/*` |
| Products | `/app-api/product/*` | `/admin-api/product/*` |
| Orders | `/app-api/order/*` | `/admin-api/order/*` |
| Store | `/app-api/store/*` | `/admin-api/store/*` |
| Coupons | `/app-api/coupon/*` | `/admin-api/coupon/*` |
| Score | `/app-api/score/*` | `/admin-api/score/*` |

## License

MIT
