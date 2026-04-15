from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Integer, BigInteger, DECIMAL, DateTime, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import BaseMixin


class MemberUser(BaseMixin, Base):
    """会员用户表"""
    __tablename__ = "go2run_user"

    nickname: Mapped[Optional[str]] = mapped_column(String(255), comment="用户昵称")
    avatar: Mapped[Optional[str]] = mapped_column(String(500), comment="用户头像")
    status: Mapped[int] = mapped_column(Integer, default=0, comment="帐号状态")
    mobile: Mapped[Optional[str]] = mapped_column(String(20), index=True, comment="手机")
    password: Mapped[Optional[str]] = mapped_column(String(255), comment="密码")
    register_ip: Mapped[Optional[str]] = mapped_column(String(50), comment="注册IP")
    login_ip: Mapped[Optional[str]] = mapped_column(String(50), comment="最后登录IP")
    login_date: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="最后登录时间")
    username: Mapped[Optional[str]] = mapped_column(String(100), index=True, comment="用户账户")
    real_name: Mapped[Optional[str]] = mapped_column(String(100), comment="真实姓名")
    birthday: Mapped[Optional[str]] = mapped_column(String(20), comment="生日")
    card_id: Mapped[Optional[str]] = mapped_column(String(50), comment="身份证号码")
    mark: Mapped[Optional[str]] = mapped_column(String(500), comment="用户备注")
    now_money: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="用户余额")
    brokerage_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="佣金金额")
    integral: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="用户剩余积分")
    sign_num: Mapped[int] = mapped_column(Integer, default=0, comment="连续签到天数")
    level: Mapped[int] = mapped_column(Integer, default=0, comment="等级")
    spread_uid: Mapped[Optional[int]] = mapped_column(BigInteger, comment="推广员id")
    spread_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="推广员关联时间")
    user_type: Mapped[Optional[str]] = mapped_column(String(50), comment="用户类型")
    is_promoter: Mapped[int] = mapped_column(Integer, default=0, comment="是否为推广员")
    pay_count: Mapped[int] = mapped_column(Integer, default=0, comment="用户购买次数")
    spread_count: Mapped[int] = mapped_column(Integer, default=0, comment="下级人数")
    addres: Mapped[Optional[str]] = mapped_column(String(500), comment="详细地址")
    login_type: Mapped[Optional[str]] = mapped_column(String(50), comment="用户登陆类型")
    openid: Mapped[Optional[str]] = mapped_column(String(255), comment="公众号openid")
    routine_openid: Mapped[Optional[str]] = mapped_column(String(255), comment="小程序openid")
    gender: Mapped[int] = mapped_column(Integer, default=0, comment="性别")


class UserAddress(BaseMixin, Base):
    """用户地址表"""
    __tablename__ = "go2run_user_address"

    uid: Mapped[int] = mapped_column(BigInteger, index=True, comment="用户id")
    real_name: Mapped[Optional[str]] = mapped_column(String(100), comment="收货人姓名")
    phone: Mapped[Optional[str]] = mapped_column(String(20), comment="收货人电话")
    province: Mapped[Optional[str]] = mapped_column(String(100), comment="省")
    city: Mapped[Optional[str]] = mapped_column(String(100), comment="市")
    district: Mapped[Optional[str]] = mapped_column(String(100), comment="区")
    detail: Mapped[Optional[str]] = mapped_column(String(500), comment="详细地址")
    post_code: Mapped[Optional[str]] = mapped_column(String(20), comment="邮编")
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否默认")
    lng: Mapped[Optional[str]] = mapped_column(String(50), comment="经度")
    lat: Mapped[Optional[str]] = mapped_column(String(50), comment="纬度")


class UserBill(BaseMixin, Base):
    """用户账单表"""
    __tablename__ = "go2run_user_bill"

    uid: Mapped[int] = mapped_column(BigInteger, index=True, comment="用户id")
    link_id: Mapped[Optional[str]] = mapped_column(String(100), comment="关联id")
    pm: Mapped[int] = mapped_column(Integer, default=0, comment="0=支出,1=获得")
    title: Mapped[Optional[str]] = mapped_column(String(255), comment="账单标题")
    category: Mapped[Optional[str]] = mapped_column(String(100), comment="明细种类")
    type: Mapped[Optional[str]] = mapped_column(String(100), comment="明细类型")
    number: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="明细数字")
    balance: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="剩余")
    mark: Mapped[Optional[str]] = mapped_column(String(500), comment="备注")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="0待确认1有效")
