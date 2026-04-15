import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, Query, UploadFile, File
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_admin_id
from app.models.store import StoreShop
from app.schemas.store import StoreShopCreateRequest, StoreShopUpdateRequest
from app.services import store as store_service
from app.utils.response import success, page_result

UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent.parent / "static" / "uploads"

router = APIRouter(prefix="/store", tags=["管理-门店"], dependencies=[Depends(get_current_admin_id)])


@router.get("/shop/list")
async def get_shops(
    page: int = Query(1, alias="pageNo"),
    page_size: int = Query(10, alias="pageSize"),
    db: AsyncSession = Depends(get_db),
):
    """获取门店列表"""
    data = await store_service.admin_get_shops(db, page, page_size)
    items = [
        {
            "id": s.id, "name": s.name, "mobile": s.mobile,
            "image": s.image, "address": s.address, "status": s.status,
            "lng": s.lng, "lat": s.lat,
            "createTime": s.create_time.isoformat() if s.create_time else None,
        }
        for s in data["list"]
    ]
    return page_result(items, data["total"], page, page_size)


@router.post("/shop/create")
async def create_shop(req: StoreShopCreateRequest, db: AsyncSession = Depends(get_db)):
    """创建门店"""
    shop_id = await store_service.admin_create_shop(db, req)
    return success({"id": shop_id})


@router.put("/shop/update")
async def update_shop(req: StoreShopUpdateRequest, db: AsyncSession = Depends(get_db)):
    """更新门店"""
    await store_service.admin_update_shop(db, req)
    return success(msg="更新成功")


@router.delete("/shop/delete")
async def delete_shop(id: int = Query(...), db: AsyncSession = Depends(get_db)):
    """删除门店"""
    await store_service.admin_delete_shop(db, id)
    return success(msg="删除成功")


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """上传文件（图片等）"""
    ext = Path(file.filename or "file").suffix or ".jpg"
    filename = f"{uuid.uuid4().hex[:12]}{ext}"
    dest = UPLOAD_DIR / filename
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    content = await file.read()
    dest.write_bytes(content)
    return success({"url": f"/static/uploads/{filename}"})


@router.get("/shop/settings")
async def get_shop_settings(
    shop_id: int = Query(1, alias="shopId"),
    db: AsyncSession = Depends(get_db),
):
    """获取店铺设置（Logo+主题色）"""
    shop = (await db.execute(
        select(StoreShop).where(StoreShop.id == shop_id, StoreShop.deleted == False)
    )).scalar_one_or_none()
    if not shop:
        return success({"name": "", "logo": None, "themeColor": None, "currency": "¥", "enabledLanguages": [], "defaultLanguage": "zh"})
    return success({
        "id": shop.id,
        "name": shop.name,
        "logo": shop.logo,
        "themeColor": shop.theme_color,
        "currency": shop.currency or "¥",
        "notice": shop.notice,
        "noticeI18n": shop.notice_i18n,
        "enabledLanguages": shop.enabled_languages or [],
        "defaultLanguage": shop.default_language or "zh",
    })


@router.put("/shop/settings")
async def update_shop_settings(
    req: dict,
    db: AsyncSession = Depends(get_db),
):
    """更新店铺设置（Logo+主题色）"""
    shop_id = req.get("shopId") or req.get("shop_id") or 1
    shop = (await db.execute(
        select(StoreShop).where(StoreShop.id == shop_id, StoreShop.deleted == False)
    )).scalar_one_or_none()
    if not shop:
        return success(msg="店铺不存在")
    if "logo" in req:
        shop.logo = req["logo"]
    if "themeColor" in req:
        shop.theme_color = req["themeColor"]
    if "name" in req:
        shop.name = req["name"]
    if "notice" in req:
        shop.notice = req["notice"]
    if "noticeI18n" in req:
        shop.notice_i18n = req["noticeI18n"]
    if "currency" in req:
        shop.currency = req["currency"]
    if "enabledLanguages" in req:
        valid = {"de", "fr", "zh", "en", "it", "es", "ja", "ko", "pt", "hi", "ar"}
        shop.enabled_languages = [l for l in req["enabledLanguages"] if l in valid]
    if "defaultLanguage" in req:
        shop.default_language = req["defaultLanguage"]
    await db.flush()
    return success(msg="保存成功")
