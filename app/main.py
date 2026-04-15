from contextlib import asynccontextmanager

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings

# App API routes
from app.api.app.auth import router as app_auth_router
from app.api.app.product import router as app_product_router
from app.api.app.order import router as app_order_router
from app.api.app.store import router as app_store_router
from app.api.app.coupon import router as app_coupon_router
from app.api.app.user import router as app_user_router
from app.api.app.score import router as app_score_router

# Admin API routes
from app.api.admin.auth import router as admin_auth_router
from app.api.admin.product import router as admin_product_router
from app.api.admin.order import router as admin_order_router
from app.api.admin.store import router as admin_store_router
from app.api.admin.coupon import router as admin_coupon_router
from app.api.admin.user import router as admin_user_router
from app.api.admin.score import router as admin_score_router
from app.api.admin.table import router as admin_table_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: auto-seed database if empty (first-time setup)
    try:
        import subprocess, sys
        from app.config import settings as _s
        from scripts.seed import parse_db_url, is_empty, seed
        db = parse_db_url(_s.DATABASE_URL)
        if is_empty(db):
            seed(db)
    except Exception as e:
        print(f"[seed] Skipped auto-seed: {e}")
    yield
    # Shutdown


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"code": 500, "msg": str(exc), "data": None},
    )


# ============ Register App Routes (移动端/H5) ============
app.include_router(app_auth_router, prefix="/app-api")
app.include_router(app_product_router, prefix="/app-api")
app.include_router(app_order_router, prefix="/app-api")
app.include_router(app_store_router, prefix="/app-api")
app.include_router(app_coupon_router, prefix="/app-api")
app.include_router(app_user_router, prefix="/app-api")
app.include_router(app_score_router, prefix="/app-api")

# ============ Register Admin Routes (管理后台) ============
app.include_router(admin_auth_router, prefix="/admin-api")
app.include_router(admin_product_router, prefix="/admin-api")
app.include_router(admin_order_router, prefix="/admin-api")
app.include_router(admin_store_router, prefix="/admin-api")
app.include_router(admin_coupon_router, prefix="/admin-api")
app.include_router(admin_user_router, prefix="/admin-api")
app.include_router(admin_score_router, prefix="/admin-api")
app.include_router(admin_table_router, prefix="/admin-api")


STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

# Serve static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


NO_CACHE = {"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache", "Expires": "0"}


@app.get("/")
async def root():
    """Serve H5 frontend."""
    return FileResponse(str(STATIC_DIR / "h5" / "index.html"), headers=NO_CACHE)


@app.get("/admin")
async def admin_page():
    """Serve admin panel."""
    return FileResponse(str(STATIC_DIR / "admin" / "index.html"), headers=NO_CACHE)


@app.get("/api-info")
async def api_info():
    return {"code": 0, "msg": f"{settings.APP_NAME} v{settings.APP_VERSION}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
