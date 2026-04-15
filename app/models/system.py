from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, BigInteger, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import BaseMixin


class SystemUser(BaseMixin, Base):
    """系统用户(管理员)表"""
    __tablename__ = "system_users"

    username: Mapped[str] = mapped_column(String(100), unique=True, comment="用户账号")
    password: Mapped[str] = mapped_column(String(255), comment="密码")
    nickname: Mapped[Optional[str]] = mapped_column(String(100), comment="用户昵称")
    remark: Mapped[Optional[str]] = mapped_column(String(500), comment="备注")
    dept_id: Mapped[Optional[int]] = mapped_column(BigInteger, comment="部门ID")
    post_ids: Mapped[Optional[str]] = mapped_column(JSON, comment="岗位编号数组")
    email: Mapped[Optional[str]] = mapped_column(String(100), comment="用户邮箱")
    mobile: Mapped[Optional[str]] = mapped_column(String(20), comment="手机号码")
    sex: Mapped[int] = mapped_column(Integer, default=0, comment="用户性别")
    avatar: Mapped[Optional[str]] = mapped_column(String(500), comment="头像地址")
    status: Mapped[int] = mapped_column(Integer, default=0, comment="帐号状态(0正常,1停用)")
    login_ip: Mapped[Optional[str]] = mapped_column(String(50), comment="最后登录IP")
    login_date: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="最后登录时间")


class SystemRole(BaseMixin, Base):
    """角色表"""
    __tablename__ = "system_role"

    name: Mapped[str] = mapped_column(String(100), comment="角色名称")
    code: Mapped[str] = mapped_column(String(100), unique=True, comment="角色权限字符串")
    sort: Mapped[int] = mapped_column(Integer, default=0, comment="显示顺序")
    data_scope: Mapped[int] = mapped_column(Integer, default=1, comment="数据范围")
    data_scope_dept_ids: Mapped[Optional[str]] = mapped_column(JSON, comment="数据范围部门数组")
    status: Mapped[int] = mapped_column(Integer, default=0, comment="角色状态(0正常,1停用)")
    type: Mapped[int] = mapped_column(Integer, default=1, comment="角色类型")
    remark: Mapped[Optional[str]] = mapped_column(String(500), comment="备注")


class SystemMenu(BaseMixin, Base):
    """菜单权限表"""
    __tablename__ = "system_menu"

    name: Mapped[str] = mapped_column(String(100), comment="菜单名称")
    permission: Mapped[Optional[str]] = mapped_column(String(200), comment="权限标识")
    type: Mapped[int] = mapped_column(Integer, comment="菜单类型(1目录,2菜单,3按钮)")
    sort: Mapped[int] = mapped_column(Integer, default=0, comment="显示顺序")
    parent_id: Mapped[int] = mapped_column(BigInteger, default=0, comment="父菜单ID")
    path: Mapped[Optional[str]] = mapped_column(String(255), comment="路由地址")
    icon: Mapped[Optional[str]] = mapped_column(String(100), comment="菜单图标")
    component: Mapped[Optional[str]] = mapped_column(String(255), comment="组件路径")
    component_name: Mapped[Optional[str]] = mapped_column(String(255), comment="组件名")
    status: Mapped[int] = mapped_column(Integer, default=0, comment="菜单状态(0正常,1停用)")
    visible: Mapped[bool] = mapped_column(default=True, comment="是否可见")
    keep_alive: Mapped[bool] = mapped_column(default=True, comment="是否缓存")
    always_show: Mapped[bool] = mapped_column(default=True, comment="是否总是显示")


class SystemDept(BaseMixin, Base):
    """部门表"""
    __tablename__ = "system_dept"

    name: Mapped[str] = mapped_column(String(100), comment="部门名称")
    parent_id: Mapped[int] = mapped_column(BigInteger, default=0, comment="父部门id")
    sort: Mapped[int] = mapped_column(Integer, default=0, comment="显示顺序")
    leader_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, comment="负责人")
    phone: Mapped[Optional[str]] = mapped_column(String(20), comment="联系电话")
    email: Mapped[Optional[str]] = mapped_column(String(100), comment="邮箱")
    status: Mapped[int] = mapped_column(Integer, default=0, comment="部门状态(0正常,1停用)")
