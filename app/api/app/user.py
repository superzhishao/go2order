from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user_id
from app.schemas.user import UserUpdateRequest, AddressCreateRequest, AddressUpdateRequest
from app.services import user as user_service
from app.utils.response import success

router = APIRouter(prefix="/user", tags=["用户"])


@router.get("/profile")
async def get_profile(
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取用户信息"""
    data = await user_service.get_user_profile(db, uid)
    return success(data)


@router.post("/update")
async def update_profile(
    req: UserUpdateRequest,
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """更新用户信息"""
    await user_service.update_user_profile(db, uid, req.nickname, req.avatar, req.birthday, req.real_name)
    return success(msg="更新成功")


# ============ 地址管理 ============

@router.get("/address/list")
async def get_addresses(
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取地址列表"""
    addresses = await user_service.get_user_addresses(db, uid)
    data = [
        {
            "id": a.id,
            "real_name": a.real_name,
            "phone": a.phone,
            "province": a.province,
            "city": a.city,
            "district": a.district,
            "detail": a.detail,
            "is_default": a.is_default,
        }
        for a in addresses
    ]
    return success(data)


@router.post("/address/create")
async def create_address(
    req: AddressCreateRequest,
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """新增地址"""
    addr_id = await user_service.create_address(db, uid, req.model_dump())
    return success({"id": addr_id})


@router.post("/address/update")
async def update_address(
    req: AddressUpdateRequest,
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """更新地址"""
    await user_service.update_address(db, uid, req.id, req.model_dump(exclude={"id"}))
    return success(msg="更新成功")


@router.post("/address/delete")
async def delete_address(
    id: int,
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """删除地址"""
    await user_service.delete_address(db, uid, id)
    return success(msg="删除成功")
