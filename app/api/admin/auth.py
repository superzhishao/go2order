from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_admin_id
from app.schemas.auth import AdminLoginRequest
from app.services import auth as auth_service
from app.utils.response import success

router = APIRouter(prefix="/system/auth", tags=["管理员认证"])


@router.post("/login")
async def admin_login(req: AdminLoginRequest, db: AsyncSession = Depends(get_db)):
    """管理员登录"""
    data = await auth_service.admin_login(db, req.username, req.password)
    return success(data)


@router.post("/logout")
async def admin_logout():
    """管理员退出"""
    return success(msg="退出成功")


@router.get("/get-permission-info")
async def get_permission_info(admin_id: int = Depends(get_current_admin_id)):
    """获取权限信息（简化版）"""
    return success({
        "roles": ["admin"],
        "permissions": ["*:*:*"],
        "user": {"id": admin_id},
    })
