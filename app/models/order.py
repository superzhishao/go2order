from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Integer, BigInteger, DECIMAL, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import BaseMixin


class StoreOrder(BaseMixin, Base):
    """订单表"""
    __tablename__ = "go2run_store_order"

    order_id: Mapped[str] = mapped_column(String(50), unique=True, comment="订单号")
    extend_order_id: Mapped[Optional[str]] = mapped_column(String(50), comment="额外订单号")
    uid: Mapped[int] = mapped_column(BigInteger, index=True, comment="用户id")
    real_name: Mapped[Optional[str]] = mapped_column(String(100), comment="用户姓名")
    user_phone: Mapped[Optional[str]] = mapped_column(String(20), comment="用户电话")
    user_address: Mapped[Optional[str]] = mapped_column(String(500), comment="详细地址")
    cart_id: Mapped[Optional[str]] = mapped_column(String(500), comment="购物车id")
    freight_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="运费金额")
    total_num: Mapped[int] = mapped_column(Integer, default=0, comment="订单商品总数")
    total_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="订单总价")
    total_postage: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="邮费")
    pay_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="实际支付金额")
    pay_postage: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="支付邮费")
    deduction_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="抵扣金额")
    coupon_id: Mapped[int] = mapped_column(Integer, default=0, comment="优惠券id")
    coupon_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="优惠券金额")
    paid: Mapped[int] = mapped_column(Integer, default=0, comment="支付状态")
    pay_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="支付时间")
    pay_type: Mapped[Optional[str]] = mapped_column(String(50), comment="支付方式")
    order_type: Mapped[Optional[str]] = mapped_column(String(50), default="takein", comment="订单类型(takein自取,takeout外卖)")
    status: Mapped[int] = mapped_column(Integer, default=0, comment="订单状态(-1申请退款,-2退货成功,0待发货,1待收货,2已收货,3已完成)")
    refund_status: Mapped[int] = mapped_column(Integer, default=0, comment="0未退款 1申请中 2已退款")
    refund_reason_wap_img: Mapped[Optional[str]] = mapped_column(Text, comment="退款图片")
    refund_reason_wap_explain: Mapped[Optional[str]] = mapped_column(String(500), comment="退款用户说明")
    refund_reason_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="退款时间")
    refund_reason_wap: Mapped[Optional[str]] = mapped_column(String(500), comment="前台退款原因")
    refund_reason: Mapped[Optional[str]] = mapped_column(String(500), comment="不退款的理由")
    refund_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="退款金额")
    delivery_sn: Mapped[Optional[str]] = mapped_column(String(100), comment="快递公司编号")
    delivery_name: Mapped[Optional[str]] = mapped_column(String(100), comment="快递名称")
    delivery_type: Mapped[Optional[str]] = mapped_column(String(50), comment="发货类型")
    delivery_id: Mapped[Optional[str]] = mapped_column(String(100), comment="快递单号")
    delivery_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="发货时间")
    gain_integral: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="消费赚取积分")
    use_integral: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="使用积分")
    pay_integral: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="实际支付积分")
    back_integral: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="退还积分")
    mark: Mapped[Optional[str]] = mapped_column(String(500), comment="备注")
    unique: Mapped[Optional[str]] = mapped_column("unique", String(100), comment="唯一id")
    remark: Mapped[Optional[str]] = mapped_column(String(500), comment="管理员备注")
    cost: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="成本价")
    verify_code: Mapped[Optional[str]] = mapped_column(String(50), comment="核销码")
    store_id: Mapped[int] = mapped_column(Integer, default=0, comment="门店id")
    shipping_type: Mapped[int] = mapped_column(Integer, default=1, comment="配送方式(1快递,2门店自提)")
    is_channel: Mapped[int] = mapped_column(Integer, default=0, comment="支付渠道")
    is_system_del: Mapped[int] = mapped_column(Integer, default=0, comment="系统删除")
    shop_id: Mapped[int] = mapped_column(BigInteger, default=0, comment="门店ID")
    shop_name: Mapped[Optional[str]] = mapped_column(String(255), comment="门店名称")
    get_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="取餐时间")
    number_id: Mapped[Optional[int]] = mapped_column(BigInteger, comment="取餐标号")
    table_no: Mapped[Optional[str]] = mapped_column(String(50), default=None, comment="桌号")
    out_trade_no: Mapped[Optional[str]] = mapped_column(String(100), comment="外部交易号")


class StoreOrderCartInfo(Base):
    """订单购物详情表"""
    __tablename__ = "go2run_store_order_cart_info"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    oid: Mapped[int] = mapped_column(BigInteger, index=True, comment="订单id")
    order_id: Mapped[Optional[str]] = mapped_column(String(50), comment="订单号")
    cart_id: Mapped[int] = mapped_column(BigInteger, default=0, comment="购物车id")
    product_id: Mapped[int] = mapped_column(BigInteger, comment="商品ID")
    cart_info: Mapped[Optional[str]] = mapped_column(Text, comment="购物车详细信息")
    unique: Mapped[Optional[str]] = mapped_column("unique", String(100), comment="唯一id")
    is_after_sales: Mapped[int] = mapped_column(Integer, default=0, comment="是否能售后(0不能1能)")
    title: Mapped[Optional[str]] = mapped_column(String(255), comment="商品名称")
    image: Mapped[Optional[str]] = mapped_column(String(500), comment="商品图片")
    number: Mapped[int] = mapped_column(Integer, default=1, comment="数量")
    spec: Mapped[Optional[str]] = mapped_column(String(255), comment="规格")
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0, comment="价格")
    cancelled: Mapped[int] = mapped_column(Integer, default=0, comment="是否退单(0否1是)")


class StoreOrderStatus(Base):
    """订单状态表"""
    __tablename__ = "go2run_store_order_status"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    oid: Mapped[int] = mapped_column(BigInteger, index=True, comment="订单id")
    change_type: Mapped[Optional[str]] = mapped_column(String(50), comment="操作类型")
    change_message: Mapped[Optional[str]] = mapped_column(String(500), comment="操作备注")
    change_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment="操作时间")


class OrderNumber(Base):
    """取餐号表"""
    __tablename__ = "go2run_order_number"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    shop_id: Mapped[int] = mapped_column(BigInteger, comment="门店id")
    number: Mapped[int] = mapped_column(Integer, default=0, comment="当前取餐号")
    date_str: Mapped[Optional[str]] = mapped_column(String(20), comment="日期字符串")
