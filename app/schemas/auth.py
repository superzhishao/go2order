from typing import Optional
from pydantic import BaseModel


class LoginRequest(BaseModel):
    """手机号+密码登录"""
    phone: str
    password: str


class SmsLoginRequest(BaseModel):
    """手机号+验证码登录"""
    phone: str
    code: str


class SmsSendRequest(BaseModel):
    """发送验证码"""
    phone: str
    scene: int = 1  # 1登录 2注册 3修改密码


class WxMiniLoginRequest(BaseModel):
    """微信小程序登录"""
    code: str
    encrypted_data: Optional[str] = None
    iv: Optional[str] = None
    spread_uid: Optional[int] = None


class UpdatePasswordRequest(BaseModel):
    """修改密码"""
    old_password: str
    new_password: str


class RefreshTokenRequest(BaseModel):
    """刷新token"""
    refresh_token: str


class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str
    refresh_token: str
    user_id: int
    nickname: Optional[str] = None
    avatar: Optional[str] = None


class AdminLoginRequest(BaseModel):
    """管理员登录"""
    username: str
    password: str
    captcha_code: Optional[str] = None
