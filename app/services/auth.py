from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import MemberUser
from app.models.system import SystemUser
from app.utils.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token,
)


async def member_login_by_phone(db: AsyncSession, phone: str, password: str) -> dict:
    """会员手机号+密码登录"""
    stmt = select(MemberUser).where(MemberUser.mobile == phone, MemberUser.deleted == False)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="用户不存在")
    if not user.password or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="密码错误")
    if user.status != 0:
        raise HTTPException(status_code=400, detail="账号已被禁用")

    user.login_ip = ""
    user.login_date = datetime.now(timezone.utc)
    await db.flush()

    return {
        "access_token": create_access_token(user.id, "member"),
        "refresh_token": create_refresh_token(user.id, "member"),
        "user_id": user.id,
        "nickname": user.nickname,
        "avatar": user.avatar,
    }


async def member_sms_login(db: AsyncSession, phone: str, code: str) -> dict:
    """会员手机号+验证码登录（自动注册）"""
    # TODO: 验证短信验证码 (对接短信服务)
    if code != "9999":  # 默认验证码
        raise HTTPException(status_code=400, detail="验证码错误")

    stmt = select(MemberUser).where(MemberUser.mobile == phone, MemberUser.deleted == False)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        # 自动注册
        user = MemberUser(
            mobile=phone,
            nickname=f"用户{phone[-4:]}",
            status=0,
            login_type="h5",
        )
        db.add(user)
        await db.flush()

    user.login_date = datetime.now(timezone.utc)
    await db.flush()

    return {
        "access_token": create_access_token(user.id, "member"),
        "refresh_token": create_refresh_token(user.id, "member"),
        "user_id": user.id,
        "nickname": user.nickname,
        "avatar": user.avatar,
    }


async def member_wx_mini_login(db: AsyncSession, code: str, encrypted_data: Optional[str] = None,
                                iv: Optional[str] = None) -> dict:
    """微信小程序登录"""
    # TODO: 调用微信接口获取openid和session_key
    # 这里需要对接微信API: https://api.weixin.qq.com/sns/jscode2session
    raise HTTPException(status_code=501, detail="微信小程序登录需要配置APP_ID和APP_SECRET")


async def refresh_member_token(db: AsyncSession, refresh_token: str) -> dict:
    """刷新会员token"""
    payload = decode_token(refresh_token)
    if not payload or not payload.get("refresh"):
        raise HTTPException(status_code=400, detail="refresh_token无效")
    user_id = int(payload["sub"])

    stmt = select(MemberUser).where(MemberUser.id == user_id, MemberUser.deleted == False)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="用户不存在")

    return {
        "access_token": create_access_token(user.id, "member"),
        "refresh_token": create_refresh_token(user.id, "member"),
        "user_id": user.id,
        "nickname": user.nickname,
        "avatar": user.avatar,
    }


async def update_member_password(db: AsyncSession, user_id: int, old_password: str, new_password: str):
    """修改会员密码"""
    stmt = select(MemberUser).where(MemberUser.id == user_id, MemberUser.deleted == False)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="用户不存在")
    if user.password and not verify_password(old_password, user.password):
        raise HTTPException(status_code=400, detail="原密码错误")

    user.password = hash_password(new_password)
    await db.flush()


# ============ Admin Auth ============

async def admin_login(db: AsyncSession, username: str, password: str) -> dict:
    """管理员登录"""
    stmt = select(SystemUser).where(SystemUser.username == username, SystemUser.deleted == False)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="用户不存在")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="密码错误")
    if user.status != 0:
        raise HTTPException(status_code=400, detail="账号已被禁用")

    user.login_date = datetime.now(timezone.utc)
    await db.flush()

    return {
        "access_token": create_access_token(user.id, "admin"),
        "refresh_token": create_refresh_token(user.id, "admin"),
        "user_id": user.id,
        "nickname": user.nickname,
        "avatar": user.avatar,
    }
