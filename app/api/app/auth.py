from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user_id
from app.schemas.auth import (
    LoginRequest, SmsLoginRequest, SmsSendRequest,
    WxMiniLoginRequest, UpdatePasswordRequest, RefreshTokenRequest,
)
from app.services import auth as auth_service
from app.utils.response import success

router = APIRouter(prefix="/member/auth", tags=["会员认证"])


@router.post("/login")
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    """手机号+密码登录"""
    data = await auth_service.member_login_by_phone(db, req.phone, req.password)
    return success(data)


@router.post("/sms-login")
async def sms_login(req: SmsLoginRequest, db: AsyncSession = Depends(get_db)):
    """手机号+验证码登录"""
    data = await auth_service.member_sms_login(db, req.phone, req.code)
    return success(data)


@router.post("/send-sms-code")
async def send_sms_code(req: SmsSendRequest):
    """发送短信验证码"""
    # TODO: 对接短信服务
    return success(msg="验证码已发送（测试环境默认验证码: 9999）")


@router.post("/weixin-mini-app-login")
async def wx_mini_login(req: WxMiniLoginRequest, db: AsyncSession = Depends(get_db)):
    """微信小程序登录"""
    data = await auth_service.member_wx_mini_login(db, req.code, req.encrypted_data, req.iv)
    return success(data)


@router.post("/refresh-token")
async def refresh_token(req: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """刷新token"""
    data = await auth_service.refresh_member_token(db, req.refresh_token)
    return success(data)


@router.post("/update-password")
async def update_password(
    req: UpdatePasswordRequest,
    uid: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """修改密码"""
    await auth_service.update_member_password(db, uid, req.old_password, req.new_password)
    return success(msg="修改成功")


@router.post("/logout")
async def logout():
    """退出登录"""
    return success(msg="退出成功")
