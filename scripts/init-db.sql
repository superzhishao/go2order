-- ==============================================
-- Go2Order Database Initialization
-- Full schema + seed data for demo/trial
-- ==============================================

CREATE DATABASE IF NOT EXISTS go2run_drink DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE go2run_drink;


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_coupon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_coupon` (
  `shop_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '店铺id(0通用)',
  `shop_name` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '店铺名称',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '优惠券名称',
  `is_switch` int NOT NULL COMMENT '是否上架',
  `least` decimal(10,2) NOT NULL COMMENT '消费多少可用',
  `value` decimal(10,2) NOT NULL COMMENT '优惠券金额',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `weigh` int NOT NULL COMMENT '权重',
  `type` int NOT NULL COMMENT '可用类型(0通用,1自取,2外卖)',
  `exchange_code` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '兑换码',
  `receive` int NOT NULL COMMENT '已领取',
  `distribute` int NOT NULL COMMENT '发行数量',
  `score` int NOT NULL COMMENT '所需积分',
  `instructions` text COLLATE utf8mb4_unicode_ci COMMENT '使用说明',
  `image` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '图片',
  `limit` int NOT NULL COMMENT '限领数量',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_coupon_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_coupon_user` (
  `uid` bigint NOT NULL COMMENT '用户id',
  `coupon_id` bigint NOT NULL COMMENT '优惠券id',
  `coupon_title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '优惠券名称',
  `coupon_value` decimal(10,2) NOT NULL COMMENT '优惠券金额',
  `coupon_least` decimal(10,2) NOT NULL COMMENT '最低消费',
  `use_time` datetime DEFAULT NULL COMMENT '使用时间',
  `start_time` datetime DEFAULT NULL COMMENT '有效开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '有效结束时间',
  `status` int NOT NULL COMMENT '状态(0未使用,1已使用,2已过期)',
  `shop_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '店铺id',
  `type` int NOT NULL COMMENT '可用类型(0通用,1自取,2外卖)',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_yshop_coupon_user_coupon_id` (`coupon_id`),
  KEY `ix_yshop_coupon_user_uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_order_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_order_number` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `shop_id` bigint NOT NULL COMMENT '门店id',
  `number` int NOT NULL COMMENT '当前取餐号',
  `date_str` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '日期字符串',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_score_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_score_order` (
  `uid` bigint NOT NULL COMMENT '用户id',
  `order_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单号',
  `product_id` bigint NOT NULL COMMENT '积分产品id',
  `product_title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '产品标题',
  `product_image` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '产品图片',
  `score` int NOT NULL COMMENT '消耗积分',
  `number` int NOT NULL COMMENT '数量',
  `total_score` int NOT NULL COMMENT '总积分',
  `real_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '收货人姓名',
  `user_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '收货人电话',
  `user_address` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '收货地址',
  `status` int NOT NULL COMMENT '状态(0待发货,1待收货,2已收货,3已完成)',
  `delivery_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '快递名称',
  `delivery_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '快递单号',
  `mark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `shop_id` bigint NOT NULL COMMENT '门店id',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  KEY `ix_yshop_score_order_uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_score_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_score_product` (
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '产品标题',
  `image` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '主图',
  `images` json DEFAULT NULL COMMENT '组图',
  `desc` text COLLATE utf8mb4_unicode_ci COMMENT '详情',
  `score` int NOT NULL COMMENT '消耗积分',
  `weigh` int NOT NULL COMMENT '权重',
  `stock` int NOT NULL COMMENT '库存',
  `sales` int NOT NULL COMMENT '销售量',
  `is_switch` int NOT NULL COMMENT '是否上架(0否,1是)',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_store_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_store_order` (
  `order_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单号',
  `extend_order_id` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '额外订单号',
  `uid` bigint NOT NULL COMMENT '用户id',
  `real_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户姓名',
  `user_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户电话',
  `user_address` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '详细地址',
  `cart_id` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '购物车id',
  `freight_price` decimal(10,2) NOT NULL COMMENT '运费金额',
  `total_num` int NOT NULL COMMENT '订单商品总数',
  `total_price` decimal(10,2) NOT NULL COMMENT '订单总价',
  `total_postage` decimal(10,2) NOT NULL COMMENT '邮费',
  `pay_price` decimal(10,2) NOT NULL COMMENT '实际支付金额',
  `pay_postage` decimal(10,2) NOT NULL COMMENT '支付邮费',
  `deduction_price` decimal(10,2) NOT NULL COMMENT '抵扣金额',
  `coupon_id` int NOT NULL COMMENT '优惠券id',
  `coupon_price` decimal(10,2) NOT NULL COMMENT '优惠券金额',
  `paid` int NOT NULL COMMENT '支付状态',
  `pay_time` datetime DEFAULT NULL COMMENT '支付时间',
  `pay_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '支付方式',
  `order_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '订单类型(takein自取,takeout外卖)',
  `status` int NOT NULL COMMENT '订单状态(-1申请退款,-2退货成功,0待发货,1待收货,2已收货,3已完成)',
  `refund_status` int NOT NULL COMMENT '0未退款 1申请中 2已退款',
  `refund_reason_wap_img` text COLLATE utf8mb4_unicode_ci COMMENT '退款图片',
  `refund_reason_wap_explain` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '退款用户说明',
  `refund_reason_time` datetime DEFAULT NULL COMMENT '退款时间',
  `refund_reason_wap` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '前台退款原因',
  `refund_reason` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '不退款的理由',
  `refund_price` decimal(10,2) NOT NULL COMMENT '退款金额',
  `delivery_sn` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '快递公司编号',
  `delivery_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '快递名称',
  `delivery_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发货类型',
  `delivery_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '快递单号',
  `delivery_time` datetime DEFAULT NULL COMMENT '发货时间',
  `gain_integral` decimal(10,2) NOT NULL COMMENT '消费赚取积分',
  `use_integral` decimal(10,2) NOT NULL COMMENT '使用积分',
  `pay_integral` decimal(10,2) NOT NULL COMMENT '实际支付积分',
  `back_integral` decimal(10,2) NOT NULL COMMENT '退还积分',
  `mark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `unique` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '唯一id',
  `remark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '管理员备注',
  `cost` decimal(10,2) NOT NULL COMMENT '成本价',
  `verify_code` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '核销码',
  `store_id` int NOT NULL COMMENT '门店id',
  `shipping_type` int NOT NULL COMMENT '配送方式(1快递,2门店自提)',
  `is_channel` int NOT NULL COMMENT '支付渠道',
  `is_system_del` int NOT NULL COMMENT '系统删除',
  `shop_id` bigint NOT NULL COMMENT '门店ID',
  `shop_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '门店名称',
  `get_time` datetime DEFAULT NULL COMMENT '取餐时间',
  `number_id` bigint DEFAULT NULL COMMENT '取餐标号',
  `table_no` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '桌号',
  `out_trade_no` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '外部交易号',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  KEY `ix_yshop_store_order_uid` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_store_order_cart_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_store_order_cart_info` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `oid` bigint NOT NULL COMMENT '订单id',
  `order_id` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '订单号',
  `cart_id` bigint NOT NULL COMMENT '购物车id',
  `product_id` bigint NOT NULL COMMENT '商品ID',
  `cart_info` text COLLATE utf8mb4_unicode_ci COMMENT '购物车详细信息',
  `unique` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '唯一id',
  `is_after_sales` int NOT NULL COMMENT '是否能售后(0不能1能)',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '商品名称',
  `image` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '商品图片',
  `number` int NOT NULL COMMENT '数量',
  `spec` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '规格',
  `price` decimal(10,2) NOT NULL COMMENT '价格',
  `cancelled` tinyint(1) DEFAULT '0' COMMENT '是否退单(0否1是)',
  PRIMARY KEY (`id`),
  KEY `ix_yshop_store_order_cart_info_oid` (`oid`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_store_order_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_store_order_status` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `oid` bigint NOT NULL COMMENT '订单id',
  `change_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '操作类型',
  `change_message` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '操作备注',
  `change_time` datetime DEFAULT NULL COMMENT '操作时间',
  PRIMARY KEY (`id`),
  KEY `ix_yshop_store_order_status_oid` (`oid`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_store_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_store_product` (
  `shop_id` int NOT NULL COMMENT '店铺id',
  `shop_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '店铺名称',
  `image` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '商品图片',
  `slider_image` text COLLATE utf8mb4_unicode_ci COMMENT '轮播图',
  `store_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '商品名称',
  `store_name_i18n` json DEFAULT NULL COMMENT '商品名称多语言',
  `store_info` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '商品简介',
  `store_info_i18n` json DEFAULT NULL COMMENT '商品简介多语言',
  `keyword` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '关键字',
  `bar_code` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '产品条码',
  `cate_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '分类id',
  `brand_id` bigint DEFAULT NULL COMMENT '品牌id',
  `price` decimal(10,2) NOT NULL COMMENT '商品价格',
  `vip_price` decimal(10,2) NOT NULL COMMENT '会员价格',
  `ot_price` decimal(10,2) NOT NULL COMMENT '市场价',
  `postage` decimal(10,2) NOT NULL COMMENT '邮费',
  `unit_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '单位名',
  `sort` smallint NOT NULL COMMENT '排序',
  `sales` int NOT NULL COMMENT '销量',
  `stock` int NOT NULL COMMENT '库存',
  `is_show` int NOT NULL COMMENT '状态(0未上架,1上架)',
  `is_hot` tinyint(1) NOT NULL COMMENT '是否热卖',
  `is_benefit` tinyint(1) NOT NULL COMMENT '是否优惠',
  `is_best` tinyint(1) NOT NULL COMMENT '是否精品',
  `is_new` int NOT NULL COMMENT '是否新品',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '产品描述',
  `description_i18n` json DEFAULT NULL COMMENT '产品描述多语言',
  `is_postage` int NOT NULL COMMENT '是否包邮',
  `give_integral` decimal(10,2) NOT NULL COMMENT '获得积分',
  `cost` decimal(10,2) NOT NULL COMMENT '成本价',
  `is_good` tinyint(1) NOT NULL COMMENT '是否优品推荐',
  `ficti` int NOT NULL COMMENT '虚拟销量',
  `browse` int NOT NULL COMMENT '浏览量',
  `is_sub` tinyint(1) NOT NULL COMMENT '是否单独分佣',
  `temp_id` int NOT NULL COMMENT '运费模板ID',
  `spec_type` int NOT NULL COMMENT '规格 0单 1多',
  `is_integral` int NOT NULL COMMENT '是否开启积分兑换',
  `integral` int NOT NULL COMMENT '需要多少积分兑换',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_store_product_attr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_store_product_attr` (
  `product_id` bigint NOT NULL COMMENT '商品ID',
  `attr_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '属性名',
  `attr_values` text COLLATE utf8mb4_unicode_ci COMMENT '属性值',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_yshop_store_product_attr_product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_store_product_attr_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_store_product_attr_result` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_id` bigint NOT NULL COMMENT '商品ID',
  `result` text COLLATE utf8mb4_unicode_ci COMMENT '商品属性参数',
  `change_time` int DEFAULT NULL COMMENT '变动时间',
  PRIMARY KEY (`id`),
  KEY `ix_yshop_store_product_attr_result_product_id` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_store_product_attr_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_store_product_attr_value` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_id` bigint NOT NULL COMMENT '商品ID',
  `sku` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '商品属性索引值',
  `stock` int NOT NULL COMMENT '属性对应的库存',
  `sales` int NOT NULL COMMENT '销量',
  `price` decimal(10,2) NOT NULL COMMENT '属性金额',
  `image` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '图片',
  `unique` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '唯一值',
  `cost` decimal(10,2) NOT NULL COMMENT '成本价',
  `bar_code` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '商品条码',
  `ot_price` decimal(10,2) NOT NULL COMMENT '原价',
  `weight` decimal(10,2) NOT NULL COMMENT '重量',
  `volume` decimal(10,2) NOT NULL COMMENT '体积',
  `integral` int NOT NULL COMMENT '需要多少积分兑换',
  PRIMARY KEY (`id`),
  KEY `ix_yshop_store_product_attr_value_product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_store_product_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_store_product_category` (
  `shop_id` int NOT NULL COMMENT '店铺id',
  `shop_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '店铺名称',
  `parent_id` bigint NOT NULL COMMENT '父分类编号',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '分类名称',
  `name_i18n` json DEFAULT NULL COMMENT '分类名称多语言',
  `pic_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '分类图片',
  `sort` int NOT NULL COMMENT '分类排序',
  `description` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '分类描述',
  `status` int NOT NULL COMMENT '开启状态',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_store_product_reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_store_product_reply` (
  `uid` bigint NOT NULL COMMENT '用户id',
  `oid` bigint NOT NULL COMMENT '订单id',
  `product_id` bigint NOT NULL COMMENT '商品id',
  `product_score` int NOT NULL COMMENT '商品分数',
  `service_score` int NOT NULL COMMENT '服务分数',
  `comment` text COLLATE utf8mb4_unicode_ci COMMENT '评论内容',
  `pics` text COLLATE utf8mb4_unicode_ci COMMENT '评论图片',
  `merchant_reply_content` text COLLATE utf8mb4_unicode_ci COMMENT '管理员回复内容',
  `is_reply` int NOT NULL COMMENT '0未回复1已回复',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_yshop_store_product_reply_product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_store_product_rule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_store_product_rule` (
  `rule_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '规格名称',
  `rule_value` text COLLATE utf8mb4_unicode_ci COMMENT '规格值',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_store_shop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_store_shop` (
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '店铺名称',
  `mobile` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '店铺电话',
  `image` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '图片',
  `images` json DEFAULT NULL COMMENT '多张图片',
  `address` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '详细地址',
  `address_map` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '地图定位地址',
  `lng` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '经度',
  `lat` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '纬度',
  `distance` int NOT NULL COMMENT '外卖配送距离(千米),0不送外卖',
  `min_price` decimal(10,2) NOT NULL COMMENT '起送价钱',
  `delivery_price` decimal(10,2) NOT NULL COMMENT '配送价格',
  `notice` text COLLATE utf8mb4_unicode_ci COMMENT '公告',
  `notice_i18n` json DEFAULT NULL COMMENT '公告多语言',
  `status` int NOT NULL COMMENT '是否营业(0否,1是)',
  `admin_id` json DEFAULT NULL COMMENT '管理员id',
  `uniprint_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '打印机id',
  `start_time` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '营业开始时间',
  `end_time` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '营业结束时间',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  `logo` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '餐厅Logo',
  `theme_color` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '主题色',
  `currency` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT '¥' COMMENT '货币符号',
  `enabled_languages` json DEFAULT NULL COMMENT '启用的客户端语言',
  `default_language` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '默认客户端语言',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_store_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_store_table` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `shop_id` bigint DEFAULT '1' COMMENT '门店ID',
  `table_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '桌号',
  `area` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '区域',
  `seats` int DEFAULT '4' COMMENT '座位数',
  `status` int DEFAULT '1' COMMENT '状态(0禁用,1启用)',
  `qr_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '二维码URL',
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted` tinyint(1) DEFAULT '0',
  `tenant_id` bigint DEFAULT '0',
  `last_settled_at` datetime DEFAULT NULL COMMENT '上次结算时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_user` (
  `nickname` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户昵称',
  `avatar` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户头像',
  `status` int NOT NULL COMMENT '帐号状态',
  `mobile` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '手机',
  `password` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '密码',
  `register_ip` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '注册IP',
  `login_ip` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '最后登录IP',
  `login_date` datetime DEFAULT NULL COMMENT '最后登录时间',
  `username` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户账户',
  `real_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '真实姓名',
  `birthday` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '生日',
  `card_id` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '身份证号码',
  `mark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户备注',
  `now_money` decimal(10,2) NOT NULL COMMENT '用户余额',
  `brokerage_price` decimal(10,2) NOT NULL COMMENT '佣金金额',
  `integral` decimal(10,2) NOT NULL COMMENT '用户剩余积分',
  `sign_num` int NOT NULL COMMENT '连续签到天数',
  `level` int NOT NULL COMMENT '等级',
  `spread_uid` bigint DEFAULT NULL COMMENT '推广员id',
  `spread_time` datetime DEFAULT NULL COMMENT '推广员关联时间',
  `user_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户类型',
  `is_promoter` int NOT NULL COMMENT '是否为推广员',
  `pay_count` int NOT NULL COMMENT '用户购买次数',
  `spread_count` int NOT NULL COMMENT '下级人数',
  `addres` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '详细地址',
  `login_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户登陆类型',
  `openid` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '公众号openid',
  `routine_openid` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '小程序openid',
  `gender` int NOT NULL COMMENT '性别',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_yshop_user_mobile` (`mobile`),
  KEY `ix_yshop_user_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_user_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_user_address` (
  `uid` bigint NOT NULL COMMENT '用户id',
  `real_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '收货人姓名',
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '收货人电话',
  `province` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '省',
  `city` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '市',
  `district` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '区',
  `detail` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '详细地址',
  `post_code` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮编',
  `is_default` tinyint(1) NOT NULL COMMENT '是否默认',
  `lng` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '经度',
  `lat` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '纬度',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_yshop_user_address_uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `go2run_user_bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go2run_user_bill` (
  `uid` bigint NOT NULL COMMENT '用户id',
  `link_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '关联id',
  `pm` int NOT NULL COMMENT '0=支出,1=获得',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '账单标题',
  `category` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '明细种类',
  `type` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '明细类型',
  `number` decimal(10,2) NOT NULL COMMENT '明细数字',
  `balance` decimal(10,2) NOT NULL COMMENT '剩余',
  `mark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `status` int NOT NULL COMMENT '0待确认1有效',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_yshop_user_bill_uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `system_dept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_dept` (
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '部门名称',
  `parent_id` bigint NOT NULL COMMENT '父部门id',
  `sort` int NOT NULL COMMENT '显示顺序',
  `leader_user_id` bigint DEFAULT NULL COMMENT '负责人',
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系电话',
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `status` int NOT NULL COMMENT '部门状态(0正常,1停用)',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `system_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_menu` (
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '菜单名称',
  `permission` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '权限标识',
  `type` int NOT NULL COMMENT '菜单类型(1目录,2菜单,3按钮)',
  `sort` int NOT NULL COMMENT '显示顺序',
  `parent_id` bigint NOT NULL COMMENT '父菜单ID',
  `path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '路由地址',
  `icon` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '菜单图标',
  `component` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '组件路径',
  `component_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '组件名',
  `status` int NOT NULL COMMENT '菜单状态(0正常,1停用)',
  `visible` tinyint(1) NOT NULL COMMENT '是否可见',
  `keep_alive` tinyint(1) NOT NULL COMMENT '是否缓存',
  `always_show` tinyint(1) NOT NULL COMMENT '是否总是显示',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `system_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_role` (
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色名称',
  `code` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色权限字符串',
  `sort` int NOT NULL COMMENT '显示顺序',
  `data_scope` int NOT NULL COMMENT '数据范围',
  `data_scope_dept_ids` json DEFAULT NULL COMMENT '数据范围部门数组',
  `status` int NOT NULL COMMENT '角色状态(0正常,1停用)',
  `type` int NOT NULL COMMENT '角色类型',
  `remark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `system_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_users` (
  `username` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户账号',
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `nickname` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户昵称',
  `remark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `dept_id` bigint DEFAULT NULL COMMENT '部门ID',
  `post_ids` json DEFAULT NULL COMMENT '岗位编号数组',
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户邮箱',
  `mobile` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '手机号码',
  `sex` int NOT NULL COMMENT '用户性别',
  `avatar` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像地址',
  `status` int NOT NULL COMMENT '帐号状态(0正常,1停用)',
  `login_ip` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '最后登录IP',
  `login_date` datetime DEFAULT NULL COMMENT '最后登录时间',
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` tinyint(1) NOT NULL,
  `tenant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;


-- ==============================================
-- Seed Data
-- ==============================================


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

LOCK TABLES `go2run_store_shop` WRITE;
/*!40000 ALTER TABLE `go2run_store_shop` DISABLE KEYS */;
INSERT INTO `go2run_store_shop` (`name`, `mobile`, `image`, `images`, `address`, `address_map`, `lng`, `lat`, `distance`, `min_price`, `delivery_price`, `notice`, `notice_i18n`, `status`, `admin_id`, `uniprint_id`, `start_time`, `end_time`, `id`, `creator`, `updater`, `create_time`, `update_time`, `deleted`, `tenant_id`, `logo`, `theme_color`, `currency`, `enabled_languages`, `default_language`) VALUES ('Trattoria Bella','13800138000',NULL,NULL,'北京市朝阳区三里屯路1号',NULL,'116.454173','39.920965',5,0.00,5.00,'欢迎光临！今日新品8折','{\"ar\": \"مرحباً! خصم 20% على العناصر الجديدة اليوم\", \"de\": \"Willkommen! 20% Rabatt auf Neuheiten heute\", \"en\": \"Welcome! 20% off new items today\", \"es\": \"¡Bienvenidos! 20% de descuento en novedades hoy\", \"fr\": \"Bienvenue ! -20% sur les nouveautés aujourd hui\", \"hi\": \"स्वागत है! आज नए आइटम पर 20% की छूट\", \"it\": \"Benvenuti! Sconto 20% sulle novità di oggi\", \"ja\": \"いらっしゃいませ！本日の新商品20%OFF\", \"ko\": \"환영합니다! 오늘 신메뉴 20% 할인\", \"pt\": \"Bem-vindos! 20% de desconto nas novidades de hoje\", \"zh\": \"欢迎光临！今日新品8折\"}',1,NULL,NULL,'09:00','22:00',1,NULL,NULL,'2026-04-13 21:04:04','2026-04-15 15:40:35',0,0,'/static/uploads/9b3cba564b94.png','#33691E','€','[\"zh\", \"en\", \"de\", \"fr\", \"it\", \"es\", \"ja\", \"ko\", \"pt\", \"hi\", \"ar\"]','en');
/*!40000 ALTER TABLE `go2run_store_shop` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `go2run_store_product` WRITE;
/*!40000 ALTER TABLE `go2run_store_product` DISABLE KEYS */;
INSERT INTO `go2run_store_product` (`shop_id`, `shop_name`, `image`, `slider_image`, `store_name`, `store_name_i18n`, `store_info`, `store_info_i18n`, `keyword`, `bar_code`, `cate_id`, `brand_id`, `price`, `vip_price`, `ot_price`, `postage`, `unit_name`, `sort`, `sales`, `stock`, `is_show`, `is_hot`, `is_benefit`, `is_best`, `is_new`, `description`, `description_i18n`, `is_postage`, `give_integral`, `cost`, `is_good`, `ficti`, `browse`, `is_sub`, `temp_id`, `spec_type`, `is_integral`, `integral`, `id`, `creator`, `updater`, `create_time`, `update_time`, `deleted`, `tenant_id`) VALUES (1,NULL,'/static/uploads/products/6.jpg',NULL,'布拉塔芝士配番茄','{\"ar\": \"بوراتا مع طماطم\", \"de\": \"Burrata mit Tomaten\", \"en\": \"Burrata with Tomatoes\", \"es\": \"Burrata con Tomates\", \"fr\": \"Burrata aux Tomates\", \"hi\": \"बुर्राटा और टमाटर\", \"it\": \"Burrata con Pomodori\", \"ja\": \"ブッラータとトマト\", \"ko\": \"부라타 치즈와 토마토\", \"pt\": \"Burrata com Tomates\", \"zh\": \"布拉塔芝士配番茄\"}','新鲜Burrata奶酪搭配传家宝番茄、罗勒与特级初榨橄榄油','{\"ar\": \"بوراتا طازجة مع طماطم موروثة وريحان وزيت زيتون بكر ممتاز\", \"de\": \"Frischer Burrata mit Erbstücktomaten, Basilikum & nativem Olivenöl extra\", \"en\": \"Fresh Burrata cheese with heirloom tomatoes, basil & extra virgin olive oil\", \"es\": \"Queso Burrata fresco con tomates reliquia, albahaca y aceite de oliva virgen extra\", \"fr\": \"Burrata fraîche avec tomates anciennes, basilic et huile d\'olive extra vierge\", \"hi\": \"ताज़ा बुर्राटा चीज़, टमाटर, तुलसी और एक्स्ट्रा वर्जिन जैतून तेल\", \"it\": \"Burrata fresca con pomodori, basilico e olio extravergine d\'oliva\", \"ja\": \"フレッシュブッラータチーズ、エアルームトマト、バジル、EXVオリーブオイル\", \"ko\": \"신선한 부라타 치즈, 에어룸 토마토, 바질, 엑스트라 버진 올리브오일\", \"pt\": \"Burrata fresca com tomates tradicionais, manjericão e azeite extra virgem\", \"zh\": \"新鲜Burrata奶酪搭配传家宝番茄、罗勒与特级初榨橄榄油\"}',NULL,NULL,'4',NULL,68.00,0.00,78.00,0.00,'份',1,0,99,1,0,0,0,0,'新鲜Burrata奶酪搭配传家宝番茄、罗勒与特级初榨橄榄油','{\"ar\": \"بوراتا طازجة مع طماطم موروثة وريحان وزيت زيتون بكر ممتاز\", \"de\": \"Frischer Burrata mit Erbstücktomaten, Basilikum & nativem Olivenöl extra\", \"en\": \"Fresh Burrata cheese with heirloom tomatoes, basil & extra virgin olive oil\", \"es\": \"Queso Burrata fresco con tomates reliquia, albahaca y aceite de oliva virgen extra\", \"fr\": \"Burrata fraîche avec tomates anciennes, basilic et huile d\'olive extra vierge\", \"hi\": \"ताज़ा बुर्राटा चीज़, टमाटर, तुलसी और एक्स्ट्रा वर्जिन जैतून तेल\", \"it\": \"Burrata fresca con pomodori, basilico e olio extravergine d\'oliva\", \"ja\": \"フレッシュブッラータチーズ、エアルームトマト、バジル、EXVオリーブオイル\", \"ko\": \"신선한 부라타 치즈, 에어룸 토마토, 바질, 엑스트라 버진 올리브오일\", \"pt\": \"Burrata fresca com tomates tradicionais, manjericão e azeite extra virgem\", \"zh\": \"新鲜Burrata奶酪搭配传家宝番茄、罗勒与特级初榨橄榄油\"}',0,0.00,0.00,0,0,3,0,0,0,0,0,6,NULL,NULL,'2026-04-14 15:38:14','2026-04-15 01:43:04',0,0),(1,NULL,'/static/uploads/products/7.jpg',NULL,'帕尔马火腿蜜瓜','{\"ar\": \"لحم بارما مع شمام\", \"de\": \"Parmaschinken mit Melone\", \"en\": \"Parma Ham & Melon\", \"es\": \"Jamón de Parma con Melón\", \"fr\": \"Jambon de Parme et Melon\", \"hi\": \"पार्मा हैम और खरबूजा\", \"it\": \"Prosciutto e Melone\", \"ja\": \"パルマハムとメロン\", \"ko\": \"파르마햄과 멜론\", \"pt\": \"Presunto de Parma com Melão\", \"zh\": \"帕尔马火腿蜜瓜\"}','24个月熟成帕尔马火腿配新鲜哈密瓜与芝麻菜','{\"ar\": \"لحم بارما معتق 24 شهر مع شمام طازج وجرجير\", \"de\": \"24 Monate gereifter Parmaschinken mit frischer Melone & Rucola\", \"en\": \"24-month aged Parma ham with fresh melon & rocket\", \"es\": \"Jamón de Parma madurado 24 meses con melón fresco y rúcula\", \"fr\": \"Jambon de Parme affiné 24 mois avec melon frais et roquette\", \"hi\": \"24 महीने पुराना पार्मा हैम, ताज़ा खरबूजा और रॉकेट\", \"it\": \"Prosciutto di Parma stagionato 24 mesi con melone fresco e rucola\", \"ja\": \"24ヶ月熟成パルマハム、フレッシュメロンとルッコラ\", \"ko\": \"24개월 숙성 파르마햄, 신선한 멜론과 루꼴라\", \"pt\": \"Presunto de Parma curado 24 meses com melão fresco e rúcula\", \"zh\": \"24个月熟成帕尔马火腿配新鲜哈密瓜与芝麻菜\"}',NULL,NULL,'4',NULL,58.00,0.00,68.00,0.00,'份',2,0,99,1,0,0,0,0,'24个月熟成帕尔马火腿配新鲜哈密瓜与芝麻菜','{\"ar\": \"لحم بارما معتق 24 شهر مع شمام طازج وجرجير\", \"de\": \"24 Monate gereifter Parmaschinken mit frischer Melone & Rucola\", \"en\": \"24-month aged Parma ham with fresh melon & rocket\", \"es\": \"Jamón de Parma madurado 24 meses con melón fresco y rúcula\", \"fr\": \"Jambon de Parme affiné 24 mois avec melon frais et roquette\", \"hi\": \"24 महीने पुराना पार्मा हैम, ताज़ा खरबूजा और रॉकेट\", \"it\": \"Prosciutto di Parma stagionato 24 mesi con melone fresco e rucola\", \"ja\": \"24ヶ月熟成パルマハム、フレッシュメロンとルッコラ\", \"ko\": \"24개월 숙성 파르마햄, 신선한 멜론과 루꼴라\", \"pt\": \"Presunto de Parma curado 24 meses com melão fresco e rúcula\", \"zh\": \"24个月熟成帕尔马火腿配新鲜哈密瓜与芝麻菜\"}',0,0.00,0.00,0,0,3,0,0,0,0,0,7,NULL,NULL,'2026-04-14 15:38:14','2026-04-15 01:43:07',0,0),(1,NULL,'/static/uploads/products/8.jpg',NULL,'炸鱿鱼圈','{\"ar\": \"كالاماري مقلي\", \"de\": \"Frittierte Calamari\", \"en\": \"Fried Calamari\", \"es\": \"Calamares Fritos\", \"fr\": \"Calamars Frits\", \"hi\": \"फ्राइड कैलामारी\", \"it\": \"Calamari Fritti\", \"ja\": \"フライドカラマリ\", \"ko\": \"칼라마리 튀김\", \"pt\": \"Lulas Fritas\", \"zh\": \"炸鱿鱼圈\"}','酥脆金黄鱿鱼圈配自制蒜蓉蛋黄酱','{\"ar\": \"حلقات كالاماري مقرمشة مع أيولي ثوم منزلي\", \"de\": \"Knusprig goldene Calamari-Ringe mit hausgemachter Knoblauch-Aioli\", \"en\": \"Crispy golden calamari rings with homemade garlic aioli\", \"es\": \"Anillos de calamar crujientes con alioli de ajo casero\", \"fr\": \"Anneaux de calamars croustillants avec aïoli maison\", \"hi\": \"कुरकुरे कैलामारी रिंग, घर का बना लहसुन एओली\", \"it\": \"Anelli di calamari croccanti con aioli all\'aglio fatto in casa\", \"ja\": \"カリカリの黄金カラマリリング、自家製ガーリックアイオリ添え\", \"ko\": \"바삭한 칼라마리 링, 수제 갈릭 아이올리\", \"pt\": \"Anéis de lula crocantes com aioli de alho caseiro\", \"zh\": \"酥脆金黄鱿鱼圈配自制蒜蓉蛋黄酱\"}',NULL,NULL,'4',NULL,48.00,0.00,56.00,0.00,'份',3,0,99,1,0,0,0,0,'酥脆金黄鱿鱼圈配自制蒜蓉蛋黄酱','{\"ar\": \"حلقات كالاماري مقرمشة مع أيولي ثوم منزلي\", \"de\": \"Knusprig goldene Calamari-Ringe mit hausgemachter Knoblauch-Aioli\", \"en\": \"Crispy golden calamari rings with homemade garlic aioli\", \"es\": \"Anillos de calamar crujientes con alioli de ajo casero\", \"fr\": \"Anneaux de calamars croustillants avec aïoli maison\", \"hi\": \"कुरकुरे कैलामारी रिंग, घर का बना लहसुन एओली\", \"it\": \"Anelli di calamari croccanti con aioli all\'aglio fatto in casa\", \"ja\": \"カリカリの黄金カラマリリング、自家製ガーリックアイオリ添え\", \"ko\": \"바삭한 칼라마리 링, 수제 갈릭 아이올리\", \"pt\": \"Anéis de lula crocantes com aioli de alho caseiro\", \"zh\": \"酥脆金黄鱿鱼圈配自制蒜蓉蛋黄酱\"}',0,0.00,0.00,0,0,1,0,0,0,0,0,8,NULL,NULL,'2026-04-14 15:38:14','2026-04-15 01:39:01',0,0),(1,NULL,'/static/uploads/products/9.jpg',NULL,'凯撒沙拉','{\"ar\": \"سلطة سيزر\", \"de\": \"Caesar Salat\", \"en\": \"Caesar Salad\", \"es\": \"Ensalada César\", \"fr\": \"Salade César\", \"hi\": \"सीज़र सलाद\", \"it\": \"Insalata Caesar\", \"ja\": \"シーザーサラダ\", \"ko\": \"시저 샐러드\", \"pt\": \"Salada Caesar\", \"zh\": \"凯撒沙拉\"}','罗马生菜、帕玛森芝士、自制面包丁与经典凯撒酱','{\"ar\": \"خس روماني وبارميزان وخبز محمص منزلي وصلصة سيزر كلاسيكية\", \"de\": \"Römersalat, Parmesan, hausgemachte Croutons & klassisches Caesar-Dressing\", \"en\": \"Romaine lettuce, Parmesan, homemade croutons & classic Caesar dressing\", \"es\": \"Lechuga romana, parmesano, crutones caseros y aderezo César clásico\", \"fr\": \"Laitue romaine, parmesan, croûtons maison et sauce César classique\", \"hi\": \"रोमेन लेटस, पार्मेसन, घर के क्रूटॉन और क्लासिक सीज़र ड्रेसिंग\", \"it\": \"Lattuga romana, parmigiano, crostini fatti in casa e salsa Caesar classica\", \"ja\": \"ロメインレタス、パルメザン、自家製クルトン、クラシックシーザードレッシング\", \"ko\": \"로메인 상추, 파르메산, 수제 크루통, 클래식 시저 드레싱\", \"pt\": \"Alface romana, parmesão, croutons caseiros e molho Caesar clássico\", \"zh\": \"罗马生菜、帕玛森芝士、自制面包丁与经典凯撒酱\"}',NULL,NULL,'4',NULL,42.00,0.00,48.00,0.00,'份',4,0,99,1,0,0,0,0,'罗马生菜、帕玛森芝士、自制面包丁与经典凯撒酱','{\"ar\": \"خس روماني وبارميزان وخبز محمص منزلي وصلصة سيزر كلاسيكية\", \"de\": \"Römersalat, Parmesan, hausgemachte Croutons & klassisches Caesar-Dressing\", \"en\": \"Romaine lettuce, Parmesan, homemade croutons & classic Caesar dressing\", \"es\": \"Lechuga romana, parmesano, crutones caseros y aderezo César clásico\", \"fr\": \"Laitue romaine, parmesan, croûtons maison et sauce César classique\", \"hi\": \"रोमेन लेटस, पार्मेसन, घर के क्रूटॉन और क्लासिक सीज़र ड्रेसिंग\", \"it\": \"Lattuga romana, parmigiano, crostini fatti in casa e salsa Caesar classica\", \"ja\": \"ロメインレタス、パルメザン、自家製クルトン、クラシックシーザードレッシング\", \"ko\": \"로메인 상추, 파르메산, 수제 크루통, 클래식 시저 드레싱\", \"pt\": \"Alface romana, parmesão, croutons caseiros e molho Caesar clássico\", \"zh\": \"罗马生菜、帕玛森芝士、自制面包丁与经典凯撒酱\"}',0,0.00,0.00,0,0,1,0,0,0,0,0,9,NULL,NULL,'2026-04-14 15:38:14','2026-04-15 01:39:04',0,0),(1,NULL,'/static/uploads/products/10.jpg',NULL,'经典肉酱意面','{\"ar\": \"باستا بولونيز\", \"de\": \"Pasta Bolognese\", \"en\": \"Bolognese Pasta\", \"es\": \"Pasta Boloñesa\", \"fr\": \"Pâtes Bolognaise\", \"hi\": \"बोलोनीज़ पास्ता\", \"it\": \"Pasta al Ragù\", \"ja\": \"ボロネーゼ\", \"ko\": \"볼로네제 파스타\", \"pt\": \"Massa à Bolonhesa\", \"zh\": \"经典肉酱意面\"}','慢炖8小时博洛尼亚肉酱配手工意面','{\"ar\": \"راغو بولونيز مطبوخ 8 ساعات مع باستا يدوية الصنع\", \"de\": \"8 Stunden geschmortes Bolognese-Ragù mit hausgemachter Pasta\", \"en\": \"8-hour slow-cooked Bolognese ragù with handmade pasta\", \"es\": \"Ragú boloñesa cocido a fuego lento 8 horas con pasta artesanal\", \"fr\": \"Ragù bolognais mijoté 8 heures avec pâtes artisanales\", \"hi\": \"8 घंटे धीमी आंच पर पकाया बोलोनीज़ रागू, हस्तनिर्मित पास्ता\", \"it\": \"Ragù bolognese cotto 8 ore con pasta fatta in casa\", \"ja\": \"8時間煮込みボロネーゼラグー、手打ちパスタ\", \"ko\": \"8시간 저온 조리 볼로네제 라구, 수제 파스타\", \"pt\": \"Ragù bolonhesa cozido 8 horas com massa artesanal\", \"zh\": \"慢炖8小时博洛尼亚肉酱配手工意面\"}',NULL,NULL,'5',NULL,62.00,0.00,72.00,0.00,'份',1,0,99,1,0,0,0,0,'慢炖8小时博洛尼亚肉酱配手工意面','{\"ar\": \"راغو بولونيز مطبوخ 8 ساعات مع باستا يدوية الصنع\", \"de\": \"8 Stunden geschmortes Bolognese-Ragù mit hausgemachter Pasta\", \"en\": \"8-hour slow-cooked Bolognese ragù with handmade pasta\", \"es\": \"Ragú boloñesa cocido a fuego lento 8 horas con pasta artesanal\", \"fr\": \"Ragù bolognais mijoté 8 heures avec pâtes artisanales\", \"hi\": \"8 घंटे धीमी आंच पर पकाया बोलोनीज़ रागू, हस्तनिर्मित पास्ता\", \"it\": \"Ragù bolognese cotto 8 ore con pasta fatta in casa\", \"ja\": \"8時間煮込みボロネーゼラグー、手打ちパスタ\", \"ko\": \"8시간 저온 조리 볼로네제 라구, 수제 파스타\", \"pt\": \"Ragù bolonhesa cozido 8 horas com massa artesanal\", \"zh\": \"慢炖8小时博洛尼亚肉酱配手工意面\"}',0,0.00,0.00,0,0,0,0,0,0,0,0,10,NULL,NULL,'2026-04-14 15:38:32','2026-04-14 15:38:32',0,0),(1,NULL,'/static/uploads/products/11.jpg',NULL,'奶油培根意面','{\"ar\": \"كاربونارا\", \"de\": \"Carbonara\", \"en\": \"Carbonara\", \"es\": \"Carbonara\", \"fr\": \"Carbonara\", \"hi\": \"कार्बोनारा\", \"it\": \"Carbonara\", \"ja\": \"カルボナーラ\", \"ko\": \"카르보나라\", \"pt\": \"Carbonara\", \"zh\": \"奶油培根意面\"}','Carbonara经典做法，意大利培根、蛋黄、佩科里诺芝士','{\"ar\": \"كاربونارا كلاسيكية مع غوانشالي وصفار بيض وبيكورينو\", \"de\": \"Klassische Carbonara mit italienischem Guanciale, Eigelb & Pecorino\", \"en\": \"Classic Carbonara with Italian guanciale, egg yolk & Pecorino cheese\", \"es\": \"Carbonara clásica con guanciale italiano, yema de huevo y queso Pecorino\", \"fr\": \"Carbonara classique avec guanciale, jaune d\'œuf et pecorino\", \"hi\": \"क्लासिक कार्बोनारा, गुआन्चाले, अंडे की जर्दी और पेकोरिनो चीज़\", \"it\": \"Carbonara classica con guanciale, tuorlo d\'uovo e pecorino\", \"ja\": \"クラシックカルボナーラ、グアンチャーレ、卵黄、ペコリーノチーズ\", \"ko\": \"클래식 카르보나라, 관찰레, 달걀노른자, 페코리노 치즈\", \"pt\": \"Carbonara clássica com guanciale, gema de ovo e pecorino\", \"zh\": \"Carbonara经典做法，意大利培根、蛋黄、佩科里诺芝士\"}',NULL,NULL,'5',NULL,68.00,0.00,78.00,0.00,'份',2,0,99,1,0,0,0,0,'Carbonara经典做法，意大利培根、蛋黄、佩科里诺芝士','{\"ar\": \"كاربونارا كلاسيكية مع غوانشالي وصفار بيض وبيكورينو\", \"de\": \"Klassische Carbonara mit italienischem Guanciale, Eigelb & Pecorino\", \"en\": \"Classic Carbonara with Italian guanciale, egg yolk & Pecorino cheese\", \"es\": \"Carbonara clásica con guanciale italiano, yema de huevo y queso Pecorino\", \"fr\": \"Carbonara classique avec guanciale, jaune d\'œuf et pecorino\", \"hi\": \"क्लासिक कार्बोनारा, गुआन्चाले, अंडे की जर्दी और पेकोरिनो चीज़\", \"it\": \"Carbonara classica con guanciale, tuorlo d\'uovo e pecorino\", \"ja\": \"クラシックカルボナーラ、グアンチャーレ、卵黄、ペコリーノチーズ\", \"ko\": \"클래식 카르보나라, 관찰레, 달걀노른자, 페코리노 치즈\", \"pt\": \"Carbonara clássica com guanciale, gema de ovo e pecorino\", \"zh\": \"Carbonara经典做法，意大利培根、蛋黄、佩科里诺芝士\"}',0,0.00,0.00,0,0,0,0,0,0,0,0,11,NULL,NULL,'2026-04-14 15:38:32','2026-04-14 15:38:32',0,0),(1,NULL,'/static/uploads/products/12.jpg',NULL,'海鲜墨鱼汁意面','{\"ar\": \"باستا بحبر الحبار\", \"de\": \"Meeresfrüchte-Pasta mit Tintenfischtinte\", \"en\": \"Squid Ink Seafood Pasta\", \"es\": \"Pasta Negra de Mariscos\", \"fr\": \"Pâtes à l\'Encre de Seiche\", \"hi\": \"स्क्विड इंक सीफूड पास्ता\", \"it\": \"Pasta al Nero di Seppia\", \"ja\": \"イカ墨シーフードパスタ\", \"ko\": \"오징어먹물 해산물 파스타\", \"pt\": \"Massa Negra de Frutos do Mar\", \"zh\": \"海鲜墨鱼汁意面\"}','鲜虾、蛤蜊、鱿鱼配墨鱼汁手工意面','{\"ar\": \"جمبري ومحار وحبار مع باستا حبر الحبار يدوية الصنع\", \"de\": \"Garnelen, Muscheln & Tintenfisch mit hausgemachter Tintenfisch-Pasta\", \"en\": \"Prawns, clams & squid with handmade squid ink pasta\", \"es\": \"Langostinos, almejas y calamares con pasta artesanal de tinta de calamar\", \"fr\": \"Crevettes, palourdes et calamars avec pâtes artisanales à l\'encre de seiche\", \"hi\": \"झींगे, क्लैम और स्क्विड, हस्तनिर्मित स्क्विड इंक पास्ता\", \"it\": \"Gamberi, vongole e calamari con pasta al nero di seppia fatta in casa\", \"ja\": \"エビ、アサリ、イカのイカ墨手打ちパスタ\", \"ko\": \"새우, 조개, 오징어와 수제 오징어먹물 파스타\", \"pt\": \"Camarões, amêijoas e lulas com massa artesanal de tinta de lula\", \"zh\": \"鲜虾、蛤蜊、鱿鱼配墨鱼汁手工意面\"}',NULL,NULL,'5',NULL,78.00,0.00,88.00,0.00,'份',3,0,99,1,0,0,0,0,'鲜虾、蛤蜊、鱿鱼配墨鱼汁手工意面','{\"ar\": \"جمبري ومحار وحبار مع باستا حبر الحبار يدوية الصنع\", \"de\": \"Garnelen, Muscheln & Tintenfisch mit hausgemachter Tintenfisch-Pasta\", \"en\": \"Prawns, clams & squid with handmade squid ink pasta\", \"es\": \"Langostinos, almejas y calamares con pasta artesanal de tinta de calamar\", \"fr\": \"Crevettes, palourdes et calamars avec pâtes artisanales à l\'encre de seiche\", \"hi\": \"झींगे, क्लैम और स्क्विड, हस्तनिर्मित स्क्विड इंक पास्ता\", \"it\": \"Gamberi, vongole e calamari con pasta al nero di seppia fatta in casa\", \"ja\": \"エビ、アサリ、イカのイカ墨手打ちパスタ\", \"ko\": \"새우, 조개, 오징어와 수제 오징어먹물 파스타\", \"pt\": \"Camarões, amêijoas e lulas com massa artesanal de tinta de lula\", \"zh\": \"鲜虾、蛤蜊、鱿鱼配墨鱼汁手工意面\"}',0,0.00,0.00,0,0,0,0,0,0,0,0,12,NULL,NULL,'2026-04-14 15:38:32','2026-04-14 15:38:32',0,0),(1,NULL,'/static/uploads/products/13.jpg',NULL,'松露奶油宽面','{\"ar\": \"فيتوتشيني بكريمة الكمأة\", \"de\": \"Trüffel-Sahne-Fettuccine\", \"en\": \"Truffle Cream Fettuccine\", \"es\": \"Fettuccine con Crema de Trufa\", \"fr\": \"Fettuccine à la Crème de Truffe\", \"hi\": \"ट्रफल क्रीम फेटुचीनी\", \"it\": \"Fettuccine al Tartufo\", \"ja\": \"トリュフクリームフェットチーネ\", \"ko\": \"트러플 크림 페투치네\", \"pt\": \"Fettuccine com Creme de Trufa\", \"zh\": \"松露奶油宽面\"}','黑松露酱配手工Fettuccine宽面与帕玛森芝士','{\"ar\": \"صلصة الكمأة السوداء مع فيتوتشيني يدوية وبارميزان\", \"de\": \"Schwarze Trüffelsauce mit hausgemachten Fettuccine & Parmesan\", \"en\": \"Black truffle sauce with handmade Fettuccine & Parmesan\", \"es\": \"Salsa de trufa negra con Fettuccine artesanal y parmesano\", \"fr\": \"Sauce truffe noire avec fettuccine artisanales et parmesan\", \"hi\": \"ब्लैक ट्रफल सॉस, हस्तनिर्मित फेटुचीनी और पार्मेसन\", \"it\": \"Salsa al tartufo nero con fettuccine fatte in casa e parmigiano\", \"ja\": \"黒トリュフソース、手打ちフェットチーネ、パルメザン\", \"ko\": \"블랙 트러플 소스, 수제 페투치네, 파르메산\", \"pt\": \"Molho de trufa negra com fettuccine artesanal e parmesão\", \"zh\": \"黑松露酱配手工Fettuccine宽面与帕玛森芝士\"}',NULL,NULL,'5',NULL,88.00,0.00,98.00,0.00,'份',4,0,99,1,0,0,0,0,'黑松露酱配手工Fettuccine宽面与帕玛森芝士','{\"ar\": \"صلصة الكمأة السوداء مع فيتوتشيني يدوية وبارميزان\", \"de\": \"Schwarze Trüffelsauce mit hausgemachten Fettuccine & Parmesan\", \"en\": \"Black truffle sauce with handmade Fettuccine & Parmesan\", \"es\": \"Salsa de trufa negra con Fettuccine artesanal y parmesano\", \"fr\": \"Sauce truffe noire avec fettuccine artisanales et parmesan\", \"hi\": \"ब्लैक ट्रफल सॉस, हस्तनिर्मित फेटुचीनी और पार्मेसन\", \"it\": \"Salsa al tartufo nero con fettuccine fatte in casa e parmigiano\", \"ja\": \"黒トリュフソース、手打ちフェットチーネ、パルメザン\", \"ko\": \"블랙 트러플 소스, 수제 페투치네, 파르메산\", \"pt\": \"Molho de trufa negra com fettuccine artesanal e parmesão\", \"zh\": \"黑松露酱配手工Fettuccine宽面与帕玛森芝士\"}',0,0.00,0.00,0,0,1,0,0,0,0,0,13,NULL,NULL,'2026-04-14 15:38:32','2026-04-15 01:42:56',0,0),(1,NULL,'/static/uploads/products/14.jpg',NULL,'罗勒青酱意面','{\"ar\": \"باستا بيستو\", \"de\": \"Pesto-Pasta\", \"en\": \"Pesto Pasta\", \"es\": \"Pasta al Pesto\", \"fr\": \"Pâtes au Pesto\", \"hi\": \"पेस्टो पास्ता\", \"it\": \"Pasta al Pesto\", \"ja\": \"ジェノベーゼパスタ\", \"ko\": \"페스토 파스타\", \"pt\": \"Massa ao Pesto\", \"zh\": \"罗勒青酱意面\"}','新鲜罗勒Pesto青酱配松子与帕玛森芝士','{\"ar\": \"بيستو ريحان طازج مع صنوبر وبارميزان\", \"de\": \"Frisches Basilikum-Pesto mit Pinienkernen & Parmesan\", \"en\": \"Fresh basil pesto with pine nuts & Parmesan\", \"es\": \"Pesto fresco de albahaca con piñones y parmesano\", \"fr\": \"Pesto frais au basilic avec pignons et parmesan\", \"hi\": \"ताज़ा तुलसी पेस्टो, पाइन नट्स और पार्मेसन\", \"it\": \"Pesto fresco di basilico con pinoli e parmigiano\", \"ja\": \"フレッシュバジルペスト、松の実、パルメザン\", \"ko\": \"신선한 바질 페스토, 잣, 파르메산\", \"pt\": \"Pesto fresco de manjericão com pinhões e parmesão\", \"zh\": \"新鲜罗勒Pesto青酱配松子与帕玛森芝士\"}',NULL,NULL,'5',NULL,56.00,0.00,66.00,0.00,'份',5,0,99,1,0,0,0,0,'新鲜罗勒Pesto青酱配松子与帕玛森芝士','{\"ar\": \"بيستو ريحان طازج مع صنوبر وبارميزان\", \"de\": \"Frisches Basilikum-Pesto mit Pinienkernen & Parmesan\", \"en\": \"Fresh basil pesto with pine nuts & Parmesan\", \"es\": \"Pesto fresco de albahaca con piñones y parmesano\", \"fr\": \"Pesto frais au basilic avec pignons et parmesan\", \"hi\": \"ताज़ा तुलसी पेस्टो, पाइन नट्स और पार्मेसन\", \"it\": \"Pesto fresco di basilico con pinoli e parmigiano\", \"ja\": \"フレッシュバジルペスト、松の実、パルメザン\", \"ko\": \"신선한 바질 페스토, 잣, 파르메산\", \"pt\": \"Pesto fresco de manjericão com pinhões e parmesão\", \"zh\": \"新鲜罗勒Pesto青酱配松子与帕玛森芝士\"}',0,0.00,0.00,0,0,1,0,0,0,0,0,14,NULL,NULL,'2026-04-14 15:38:32','2026-04-15 01:42:08',0,0),(1,NULL,'/static/uploads/products/15.jpg',NULL,'玛格丽特披萨','{\"ar\": \"بيتزا مارغريتا\", \"de\": \"Pizza Margherita\", \"en\": \"Margherita Pizza\", \"es\": \"Pizza Margherita\", \"fr\": \"Pizza Margherita\", \"hi\": \"मार्गेरीटा पिज़्ज़ा\", \"it\": \"Pizza Margherita\", \"ja\": \"マルゲリータピザ\", \"ko\": \"마르게리타 피자\", \"pt\": \"Pizza Margherita\", \"zh\": \"玛格丽特披萨\"}','经典Margherita，水牛马苏里拉、圣马力诺番茄酱、新鲜罗勒','{\"ar\": \"مارغريتا كلاسيكية مع موزاريلا جاموس وصلصة طماطم سان مارزانو وريحان طازج\", \"de\": \"Klassische Margherita mit Büffelmozzarella, San-Marzano-Tomatensauce & frischem Basilikum\", \"en\": \"Classic Margherita with buffalo mozzarella, San Marzano tomato sauce & fresh basil\", \"es\": \"Margherita clásica con mozzarella de búfala, salsa de tomate San Marzano y albahaca fresca\", \"fr\": \"Margherita classique avec mozzarella di bufala, sauce tomate San Marzano et basilic frais\", \"hi\": \"क्लासिक मार्गेरीटा, भैंस मोज़ेरेला, सैन मार्ज़ानो टमाटर सॉस, ताज़ा तुलसी\", \"it\": \"Margherita classica con mozzarella di bufala, pomodoro San Marzano e basilico fresco\", \"ja\": \"クラシックマルゲリータ、水牛モッツァレラ、サンマルツァーノトマトソース、フレッシュバジル\", \"ko\": \"클래식 마르게리타, 버팔로 모짜렐라, 산 마르자노 토마토 소스, 신선한 바질\", \"pt\": \"Margherita clássica com mozzarella de búfala, molho San Marzano e manjericão fresco\", \"zh\": \"经典Margherita，水牛马苏里拉、圣马力诺番茄酱、新鲜罗勒\"}',NULL,NULL,'6',NULL,58.00,0.00,68.00,0.00,'份',1,0,99,1,0,0,0,0,'经典Margherita，水牛马苏里拉、圣马力诺番茄酱、新鲜罗勒','{\"ar\": \"مارغريتا كلاسيكية مع موزاريلا جاموس وصلصة طماطم سان مارزانو وريحان طازج\", \"de\": \"Klassische Margherita mit Büffelmozzarella, San-Marzano-Tomatensauce & frischem Basilikum\", \"en\": \"Classic Margherita with buffalo mozzarella, San Marzano tomato sauce & fresh basil\", \"es\": \"Margherita clásica con mozzarella de búfala, salsa de tomate San Marzano y albahaca fresca\", \"fr\": \"Margherita classique avec mozzarella di bufala, sauce tomate San Marzano et basilic frais\", \"hi\": \"क्लासिक मार्गेरीटा, भैंस मोज़ेरेला, सैन मार्ज़ानो टमाटर सॉस, ताज़ा तुलसी\", \"it\": \"Margherita classica con mozzarella di bufala, pomodoro San Marzano e basilico fresco\", \"ja\": \"クラシックマルゲリータ、水牛モッツァレラ、サンマルツァーノトマトソース、フレッシュバジル\", \"ko\": \"클래식 마르게리타, 버팔로 모짜렐라, 산 마르자노 토마토 소스, 신선한 바질\", \"pt\": \"Margherita clássica com mozzarella de búfala, molho San Marzano e manjericão fresco\", \"zh\": \"经典Margherita，水牛马苏里拉、圣马力诺番茄酱、新鲜罗勒\"}',0,0.00,0.00,0,0,0,0,0,0,0,0,15,NULL,NULL,'2026-04-14 15:38:46','2026-04-14 15:38:46',0,0),(1,NULL,'/static/uploads/products/16.jpg',NULL,'四季披萨','{\"ar\": \"بيتزا الفصول الأربعة\", \"de\": \"Pizza Vier Jahreszeiten\", \"en\": \"Four Seasons Pizza\", \"es\": \"Pizza Cuatro Estaciones\", \"fr\": \"Pizza Quatre Saisons\", \"hi\": \"फोर सीज़न्स पिज़्ज़ा\", \"it\": \"Pizza Quattro Stagioni\", \"ja\": \"クアトロ・スタジオーニ\", \"ko\": \"사계절 피자\", \"pt\": \"Pizza Quatro Estações\", \"zh\": \"四季披萨\"}','Quattro Stagioni四种口味：火腿、蘑菇、朝鲜蓟、黑橄榄','{\"ar\": \"كواترو ستاجيوني: لحم، فطر، خرشوف وزيتون أسود\", \"de\": \"Quattro Stagioni: Schinken, Pilze, Artischocken & schwarze Oliven\", \"en\": \"Quattro Stagioni: ham, mushrooms, artichokes & black olives\", \"es\": \"Quattro Stagioni: jamón, champiñones, alcachofas y aceitunas negras\", \"fr\": \"Quattro Stagioni: jambon, champignons, artichauts et olives noires\", \"hi\": \"क्वात्रो स्टाजिओनी: हैम, मशरूम, आर्टिचोक, काले जैतून\", \"it\": \"Quattro Stagioni: prosciutto, funghi, carciofi e olive nere\", \"ja\": \"クアトロ・スタジオーニ：ハム、マッシュルーム、アーティチョーク、黒オリーブ\", \"ko\": \"콰트로 스타지오니: 햄, 버섯, 아티초크, 블랙 올리브\", \"pt\": \"Quattro Stagioni: presunto, cogumelos, alcachofras e azeitonas pretas\", \"zh\": \"Quattro Stagioni四种口味：火腿、蘑菇、朝鲜蓟、黑橄榄\"}',NULL,NULL,'6',NULL,72.00,0.00,82.00,0.00,'份',2,0,99,1,0,0,0,0,'Quattro Stagioni四种口味：火腿、蘑菇、朝鲜蓟、黑橄榄','{\"ar\": \"كواترو ستاجيوني: لحم، فطر، خرشوف وزيتون أسود\", \"de\": \"Quattro Stagioni: Schinken, Pilze, Artischocken & schwarze Oliven\", \"en\": \"Quattro Stagioni: ham, mushrooms, artichokes & black olives\", \"es\": \"Quattro Stagioni: jamón, champiñones, alcachofas y aceitunas negras\", \"fr\": \"Quattro Stagioni: jambon, champignons, artichauts et olives noires\", \"hi\": \"क्वात्रो स्टाजिओनी: हैम, मशरूम, आर्टिचोक, काले जैतून\", \"it\": \"Quattro Stagioni: prosciutto, funghi, carciofi e olive nere\", \"ja\": \"クアトロ・スタジオーニ：ハム、マッシュルーム、アーティチョーク、黒オリーブ\", \"ko\": \"콰트로 스타지오니: 햄, 버섯, 아티초크, 블랙 올리브\", \"pt\": \"Quattro Stagioni: presunto, cogumelos, alcachofras e azeitonas pretas\", \"zh\": \"Quattro Stagioni四种口味：火腿、蘑菇、朝鲜蓟、黑橄榄\"}',0,0.00,0.00,0,0,0,0,0,0,0,0,16,NULL,NULL,'2026-04-14 15:38:46','2026-04-14 15:38:46',0,0),(1,NULL,'/static/uploads/products/17.jpg',NULL,'帕尔马火腿披萨','{\"ar\": \"بيتزا لحم بارما\", \"de\": \"Pizza mit Parmaschinken\", \"en\": \"Parma Ham Pizza\", \"es\": \"Pizza de Jamón de Parma\", \"fr\": \"Pizza au Jambon de Parme\", \"hi\": \"पार्मा हैम पिज़्ज़ा\", \"it\": \"Pizza Prosciutto e Rucola\", \"ja\": \"パルマハムピザ\", \"ko\": \"파르마햄 피자\", \"pt\": \"Pizza de Presunto de Parma\", \"zh\": \"帕尔马火腿披萨\"}','薄脆饼底配帕尔马火腿、芝麻菜与帕玛森芝士','{\"ar\": \"قاعدة رقيقة مقرمشة مع لحم بارما وجرجير وبارميزان\", \"de\": \"Dünner knuspriger Boden mit Parmaschinken, Rucola & Parmesan\", \"en\": \"Thin crispy base with Parma ham, rocket & Parmesan\", \"es\": \"Base fina crujiente con jamón de Parma, rúcula y parmesano\", \"fr\": \"Base fine croustillante avec jambon de Parme, roquette et parmesan\", \"hi\": \"पतला कुरकुरा बेस, पार्मा हैम, रॉकेट और पार्मेसन\", \"it\": \"Base sottile croccante con prosciutto di Parma, rucola e parmigiano\", \"ja\": \"薄焼きクリスピー生地、パルマハム、ルッコラ、パルメザン\", \"ko\": \"얇고 바삭한 도우, 파르마햄, 루꼴라, 파르메산\", \"pt\": \"Base fina crocante com presunto de Parma, rúcula e parmesão\", \"zh\": \"薄脆饼底配帕尔马火腿、芝麻菜与帕玛森芝士\"}',NULL,NULL,'6',NULL,78.00,0.00,88.00,0.00,'份',3,0,99,1,0,0,0,0,'薄脆饼底配帕尔马火腿、芝麻菜与帕玛森芝士','{\"ar\": \"قاعدة رقيقة مقرمشة مع لحم بارما وجرجير وبارميزان\", \"de\": \"Dünner knuspriger Boden mit Parmaschinken, Rucola & Parmesan\", \"en\": \"Thin crispy base with Parma ham, rocket & Parmesan\", \"es\": \"Base fina crujiente con jamón de Parma, rúcula y parmesano\", \"fr\": \"Base fine croustillante avec jambon de Parme, roquette et parmesan\", \"hi\": \"पतला कुरकुरा बेस, पार्मा हैम, रॉकेट और पार्मेसन\", \"it\": \"Base sottile croccante con prosciutto di Parma, rucola e parmigiano\", \"ja\": \"薄焼きクリスピー生地、パルマハム、ルッコラ、パルメザン\", \"ko\": \"얇고 바삭한 도우, 파르마햄, 루꼴라, 파르메산\", \"pt\": \"Base fina crocante com presunto de Parma, rúcula e parmesão\", \"zh\": \"薄脆饼底配帕尔马火腿、芝麻菜与帕玛森芝士\"}',0,0.00,0.00,0,0,0,0,0,0,0,0,17,NULL,NULL,'2026-04-14 15:38:46','2026-04-14 15:38:46',0,0),(1,NULL,'/static/uploads/products/18.jpg',NULL,'松露蘑菇披萨','{\"ar\": \"بيتزا الكمأة والفطر\", \"de\": \"Trüffel-Pilz-Pizza\", \"en\": \"Truffle Mushroom Pizza\", \"es\": \"Pizza de Trufa y Champiñones\", \"fr\": \"Pizza Truffe et Champignons\", \"hi\": \"ट्रफल मशरूम पिज़्ज़ा\", \"it\": \"Pizza Tartufo e Funghi\", \"ja\": \"トリュフきのこピザ\", \"ko\": \"트러플 버섯 피자\", \"pt\": \"Pizza de Trufa e Cogumelos\", \"zh\": \"松露蘑菇披萨\"}','混合蘑菇、黑松露酱、马苏里拉与百里香','{\"ar\": \"فطر مشكل وصلصة كمأة سوداء وموزاريلا وزعتر\", \"de\": \"Gemischte Pilze, schwarze Trüffelsauce, Mozzarella & Thymian\", \"en\": \"Mixed mushrooms, black truffle sauce, mozzarella & thyme\", \"es\": \"Champiñones mixtos, salsa de trufa negra, mozzarella y tomillo\", \"fr\": \"Champignons mélangés, sauce truffe noire, mozzarella et thym\", \"hi\": \"मिक्स मशरूम, ब्लैक ट्रफल सॉस, मोज़ेरेला और थाइम\", \"it\": \"Funghi misti, salsa al tartufo nero, mozzarella e timo\", \"ja\": \"ミックスきのこ、黒トリュフソース、モッツァレラ、タイム\", \"ko\": \"모듬 버섯, 블랙 트러플 소스, 모짜렐라, 타임\", \"pt\": \"Cogumelos mistos, molho de trufa negra, mozzarella e tomilho\", \"zh\": \"混合蘑菇、黑松露酱、马苏里拉与百里香\"}',NULL,NULL,'6',NULL,82.00,0.00,92.00,0.00,'份',4,1,98,1,0,0,0,0,'混合蘑菇、黑松露酱、马苏里拉与百里香','{\"ar\": \"فطر مشكل وصلصة كمأة سوداء وموزاريلا وزعتر\", \"de\": \"Gemischte Pilze, schwarze Trüffelsauce, Mozzarella & Thymian\", \"en\": \"Mixed mushrooms, black truffle sauce, mozzarella & thyme\", \"es\": \"Champiñones mixtos, salsa de trufa negra, mozzarella y tomillo\", \"fr\": \"Champignons mélangés, sauce truffe noire, mozzarella et thym\", \"hi\": \"मिक्स मशरूम, ब्लैक ट्रफल सॉस, मोज़ेरेला और थाइम\", \"it\": \"Funghi misti, salsa al tartufo nero, mozzarella e timo\", \"ja\": \"ミックスきのこ、黒トリュフソース、モッツァレラ、タイム\", \"ko\": \"모듬 버섯, 블랙 트러플 소스, 모짜렐라, 타임\", \"pt\": \"Cogumelos mistos, molho de trufa negra, mozzarella e tomilho\", \"zh\": \"混合蘑菇、黑松露酱、马苏里拉与百里香\"}',0,0.00,0.00,0,0,1,0,0,0,0,0,18,NULL,NULL,'2026-04-14 15:38:46','2026-04-15 15:21:15',0,0),(1,NULL,'/static/uploads/products/19.jpg',NULL,'米兰式炸牛排','{\"ar\": \"كوتوليتا ميلانو\", \"de\": \"Kalbsschnitzel Mailänder Art\", \"en\": \"Milanese Veal Cutlet\", \"es\": \"Chuleta de Ternera a la Milanesa\", \"fr\": \"Escalope Milanaise\", \"hi\": \"मिलानीज़ वील कटलेट\", \"it\": \"Cotoletta alla Milanese\", \"ja\": \"ミラノ風カツレツ\", \"ko\": \"밀라노식 커틀릿\", \"pt\": \"Escalope à Milanesa\", \"zh\": \"米兰式炸牛排\"}','经典Cotoletta alla Milanese，酥炸牛排配柠檬角','{\"ar\": \"كوتوليتا ميلانو الكلاسيكية، شريحة لحم مقرمشة مع ليمون\", \"de\": \"Klassisches Cotoletta alla Milanese, knusprig gebratenes Schnitzel mit Zitrone\", \"en\": \"Classic Cotoletta alla Milanese, crispy fried cutlet with lemon wedge\", \"es\": \"Cotoletta alla Milanese clásica, chuleta frita crujiente con limón\", \"fr\": \"Cotoletta alla Milanese classique, escalope panée croustillante avec citron\", \"hi\": \"क्लासिक कोतोलेटा अल्ला मिलानीज़, कुरकुरा तला हुआ कटलेट, नींबू\", \"it\": \"Classica Cotoletta alla Milanese, croccante con spicchio di limone\", \"ja\": \"クラシックなミラノ風カツレツ、サクサク衣にレモン添え\", \"ko\": \"클래식 밀라노 커틀릿, 바삭하게 튀겨 레몬 웨지 곁들임\", \"pt\": \"Cotoletta alla Milanese clássica, escalope crocante com limão\", \"zh\": \"经典Cotoletta alla Milanese，酥炸牛排配柠檬角\"}',NULL,NULL,'7',NULL,128.00,0.00,148.00,0.00,'份',1,1,98,1,0,0,0,0,'经典Cotoletta alla Milanese，酥炸牛排配柠檬角','{\"ar\": \"كوتوليتا ميلانو الكلاسيكية، شريحة لحم مقرمشة مع ليمون\", \"de\": \"Klassisches Cotoletta alla Milanese, knusprig gebratenes Schnitzel mit Zitrone\", \"en\": \"Classic Cotoletta alla Milanese, crispy fried cutlet with lemon wedge\", \"es\": \"Cotoletta alla Milanese clásica, chuleta frita crujiente con limón\", \"fr\": \"Cotoletta alla Milanese classique, escalope panée croustillante avec citron\", \"hi\": \"क्लासिक कोतोलेटा अल्ला मिलानीज़, कुरकुरा तला हुआ कटलेट, नींबू\", \"it\": \"Classica Cotoletta alla Milanese, croccante con spicchio di limone\", \"ja\": \"クラシックなミラノ風カツレツ、サクサク衣にレモン添え\", \"ko\": \"클래식 밀라노 커틀릿, 바삭하게 튀겨 레몬 웨지 곁들임\", \"pt\": \"Cotoletta alla Milanese clássica, escalope crocante com limão\", \"zh\": \"经典Cotoletta alla Milanese，酥炸牛排配柠檬角\"}',0,0.00,0.00,0,0,2,0,0,0,0,0,19,NULL,NULL,'2026-04-14 15:39:02','2026-04-15 15:21:15',0,0),(1,NULL,'/static/uploads/products/20.jpg',NULL,'香煎三文鱼','{\"ar\": \"سلمون مقلي\", \"de\": \"Gebratener Lachs\", \"en\": \"Pan-seared Salmon\", \"es\": \"Salmón a la Plancha\", \"fr\": \"Saumon Poêlé\", \"hi\": \"पैन-सियर्ड सैल्मन\", \"it\": \"Salmone in Padella\", \"ja\": \"サーモンのソテー\", \"ko\": \"팬시어드 연어\", \"pt\": \"Salmão Grelhado\", \"zh\": \"香煎三文鱼\"}','挪威三文鱼配白酒柠檬黄油酱与时令蔬菜','{\"ar\": \"سلمون نرويجي مع صلصة زبدة الليمون والنبيذ الأبيض وخضار موسمية\", \"de\": \"Norwegischer Lachs mit Weißwein-Zitronen-Buttersauce & Saisongemüse\", \"en\": \"Norwegian salmon with white wine lemon butter sauce & seasonal vegetables\", \"es\": \"Salmón noruego con salsa de mantequilla, limón y vino blanco y verduras de temporada\", \"fr\": \"Saumon norvégien avec sauce beurre citron au vin blanc et légumes de saison\", \"hi\": \"नॉर्वेजियन सैल्मन, व्हाइट वाइन लेमन बटर सॉस, मौसमी सब्ज़ियां\", \"it\": \"Salmone norvegese con salsa al burro, limone e vino bianco e verdure di stagione\", \"ja\": \"ノルウェーサーモン、白ワインレモンバターソース、季節の野菜\", \"ko\": \"노르웨이 연어, 화이트와인 레몬버터 소스, 제철 채소\", \"pt\": \"Salmão norueguês com molho de manteiga, limão e vinho branco e legumes da época\", \"zh\": \"挪威三文鱼配白酒柠檬黄油酱与时令蔬菜\"}',NULL,NULL,'7',NULL,108.00,0.00,128.00,0.00,'份',2,0,99,1,0,0,0,0,'挪威三文鱼配白酒柠檬黄油酱与时令蔬菜','{\"ar\": \"سلمون نرويجي مع صلصة زبدة الليمون والنبيذ الأبيض وخضار موسمية\", \"de\": \"Norwegischer Lachs mit Weißwein-Zitronen-Buttersauce & Saisongemüse\", \"en\": \"Norwegian salmon with white wine lemon butter sauce & seasonal vegetables\", \"es\": \"Salmón noruego con salsa de mantequilla, limón y vino blanco y verduras de temporada\", \"fr\": \"Saumon norvégien avec sauce beurre citron au vin blanc et légumes de saison\", \"hi\": \"नॉर्वेजियन सैल्मन, व्हाइट वाइन लेमन बटर सॉस, मौसमी सब्ज़ियां\", \"it\": \"Salmone norvegese con salsa al burro, limone e vino bianco e verdure di stagione\", \"ja\": \"ノルウェーサーモン、白ワインレモンバターソース、季節の野菜\", \"ko\": \"노르웨이 연어, 화이트와인 레몬버터 소스, 제철 채소\", \"pt\": \"Salmão norueguês com molho de manteiga, limão e vinho branco e legumes da época\", \"zh\": \"挪威三文鱼配白酒柠檬黄油酱与时令蔬菜\"}',0,0.00,0.00,0,0,0,0,0,0,0,0,20,NULL,NULL,'2026-04-14 15:39:02','2026-04-14 15:39:02',0,0),(1,NULL,'/static/uploads/products/21.jpg',NULL,'慢炖小牛膝','{\"ar\": \"أوسو بوكو\", \"de\": \"Osso Buco\", \"en\": \"Osso Buco\", \"es\": \"Osso Buco\", \"fr\": \"Osso Buco\", \"hi\": \"ऑसो बूको\", \"it\": \"Osso Buco\", \"ja\": \"オッソブーコ\", \"ko\": \"오소부코\", \"pt\": \"Osso Buco\", \"zh\": \"慢炖小牛膝\"}','Osso Buco经典做法，慢炖6小时配番红花烩饭','{\"ar\": \"أوسو بوكو كلاسيكي مطبوخ 6 ساعات مع ريزوتو الزعفران\", \"de\": \"Klassisches Osso Buco, 6 Stunden geschmort mit Safran-Risotto\", \"en\": \"Classic Osso Buco, 6-hour slow braised with saffron risotto\", \"es\": \"Osso Buco clásico, estofado lento 6 horas con risotto de azafrán\", \"fr\": \"Osso Buco classique, braisé 6 heures avec risotto au safran\", \"hi\": \"क्लासिक ऑसो बूको, 6 घंटे धीमी आंच पर ब्रेज़, केसर रिसोट्टो\", \"it\": \"Osso Buco classico, brasato 6 ore con risotto allo zafferano\", \"ja\": \"クラシックオッソブーコ、6時間煮込み、サフランリゾット添え\", \"ko\": \"클래식 오소부코, 6시간 저온 조림, 사프란 리소토 곁들임\", \"pt\": \"Osso Buco clássico, braseado 6 horas com risoto de açafrão\", \"zh\": \"Osso Buco经典做法，慢炖6小时配番红花烩饭\"}',NULL,NULL,'7',NULL,168.00,0.00,188.00,0.00,'份',3,0,99,1,0,0,0,0,'Osso Buco经典做法，慢炖6小时配番红花烩饭','{\"ar\": \"أوسو بوكو كلاسيكي مطبوخ 6 ساعات مع ريزوتو الزعفران\", \"de\": \"Klassisches Osso Buco, 6 Stunden geschmort mit Safran-Risotto\", \"en\": \"Classic Osso Buco, 6-hour slow braised with saffron risotto\", \"es\": \"Osso Buco clásico, estofado lento 6 horas con risotto de azafrán\", \"fr\": \"Osso Buco classique, braisé 6 heures avec risotto au safran\", \"hi\": \"क्लासिक ऑसो बूको, 6 घंटे धीमी आंच पर ब्रेज़, केसर रिसोट्टो\", \"it\": \"Osso Buco classico, brasato 6 ore con risotto allo zafferano\", \"ja\": \"クラシックオッソブーコ、6時間煮込み、サフランリゾット添え\", \"ko\": \"클래식 오소부코, 6시간 저온 조림, 사프란 리소토 곁들임\", \"pt\": \"Osso Buco clássico, braseado 6 horas com risoto de açafrão\", \"zh\": \"Osso Buco经典做法，慢炖6小时配番红花烩饭\"}',0,0.00,0.00,0,0,0,0,0,0,0,0,21,NULL,NULL,'2026-04-14 15:39:02','2026-04-14 15:39:02',0,0),(1,NULL,'/static/uploads/products/22.jpg',NULL,'烤羊排配迷迭香','{\"ar\": \"ضلوع غنم بالروزماري\", \"de\": \"Lammrack mit Rosmarin\", \"en\": \"Rosemary Lamb Rack\", \"es\": \"Costillas de Cordero al Romero\", \"fr\": \"Carré d\'Agneau au Romarin\", \"hi\": \"रोज़मेरी लैम रैक\", \"it\": \"Costolette d\'Agnello al Rosmarino\", \"ja\": \"ローズマリーラムラック\", \"ko\": \"로즈마리 양갈비\", \"pt\": \"Costeletas de Cordeiro com Alecrim\", \"zh\": \"烤羊排配迷迭香\"}','新西兰法式羊排配迷迭香大蒜黄油与烤蔬菜','{\"ar\": \"ضلوع غنم نيوزيلندية مع زبدة روزماري وثوم وخضار مشوية\", \"de\": \"Neuseeländisches Lammrack mit Rosmarin-Knoblauchbutter & Ofengemüse\", \"en\": \"NZ French-cut lamb rack with rosemary garlic butter & roasted vegetables\", \"es\": \"Costillas de cordero neozelandesas con mantequilla de romero y ajo y verduras asadas\", \"fr\": \"Carré d\'agneau néo-zélandais avec beurre romarin-ail et légumes rôtis\", \"hi\": \"न्यूज़ीलैंड लैम रैक, रोज़मेरी लहसुन मक्खन और भुनी सब्ज़ियां\", \"it\": \"Costolette d\'agnello neozelandesi con burro rosmarino-aglio e verdure arrosto\", \"ja\": \"NZ産フレンチカットラムラック、ローズマリーガーリックバター、ロースト野菜\", \"ko\": \"뉴질랜드 프렌치컷 양갈비, 로즈마리 갈릭 버터, 구운 채소\", \"pt\": \"Costeletas de cordeiro neozelandesas com manteiga de alecrim e alho e legumes assados\", \"zh\": \"新西兰法式羊排配迷迭香大蒜黄油与烤蔬菜\"}',NULL,NULL,'7',NULL,148.00,0.00,168.00,0.00,'份',4,0,99,1,0,0,0,0,'新西兰法式羊排配迷迭香大蒜黄油与烤蔬菜','{\"ar\": \"ضلوع غنم نيوزيلندية مع زبدة روزماري وثوم وخضار مشوية\", \"de\": \"Neuseeländisches Lammrack mit Rosmarin-Knoblauchbutter & Ofengemüse\", \"en\": \"NZ French-cut lamb rack with rosemary garlic butter & roasted vegetables\", \"es\": \"Costillas de cordero neozelandesas con mantequilla de romero y ajo y verduras asadas\", \"fr\": \"Carré d\'agneau néo-zélandais avec beurre romarin-ail et légumes rôtis\", \"hi\": \"न्यूज़ीलैंड लैम रैक, रोज़मेरी लहसुन मक्खन और भुनी सब्ज़ियां\", \"it\": \"Costolette d\'agnello neozelandesi con burro rosmarino-aglio e verdure arrosto\", \"ja\": \"NZ産フレンチカットラムラック、ローズマリーガーリックバター、ロースト野菜\", \"ko\": \"뉴질랜드 프렌치컷 양갈비, 로즈마리 갈릭 버터, 구운 채소\", \"pt\": \"Costeletas de cordeiro neozelandesas com manteiga de alecrim e alho e legumes assados\", \"zh\": \"新西兰法式羊排配迷迭香大蒜黄油与烤蔬菜\"}',0,0.00,0.00,0,0,2,0,0,0,0,0,22,NULL,NULL,'2026-04-14 15:39:02','2026-04-15 15:14:15',0,0),(1,NULL,'/static/uploads/products/23.jpg',NULL,'提拉米苏','{\"ar\": \"تيراميسو\", \"de\": \"Tiramisù\", \"en\": \"Tiramisù\", \"es\": \"Tiramisú\", \"fr\": \"Tiramisù\", \"hi\": \"तिरामिसू\", \"it\": \"Tiramisù\", \"ja\": \"ティラミス\", \"ko\": \"티라미수\", \"pt\": \"Tiramisù\", \"zh\": \"提拉米苏\"}','经典Tiramisù，马斯卡彭芝士、浓缩咖啡与可可粉','{\"ar\": \"تيراميسو كلاسيكي مع ماسكاربوني وإسبريسو وكاكاو\", \"de\": \"Klassisches Tiramisù mit Mascarpone, Espresso & Kakaopulver\", \"en\": \"Classic Tiramisù with mascarpone, espresso & cocoa powder\", \"es\": \"Tiramisú clásico con mascarpone, espresso y cacao en polvo\", \"fr\": \"Tiramisù classique avec mascarpone, espresso et cacao\", \"hi\": \"क्लासिक तिरामिसू, मस्कारपोन, एस्प्रेसो और कोको पाउडर\", \"it\": \"Tiramisù classico con mascarpone, espresso e cacao\", \"ja\": \"クラシックティラミス、マスカルポーネ、エスプレッソ、ココアパウダー\", \"ko\": \"클래식 티라미수, 마스카포네, 에스프레소, 코코아 파우더\", \"pt\": \"Tiramisù clássico com mascarpone, espresso e cacau\", \"zh\": \"经典Tiramisù，马斯卡彭芝士、浓缩咖啡与可可粉\"}',NULL,NULL,'8',NULL,42.00,0.00,48.00,0.00,'份',1,1,98,1,0,0,0,0,'经典Tiramisù，马斯卡彭芝士、浓缩咖啡与可可粉','{\"ar\": \"تيراميسو كلاسيكي مع ماسكاربوني وإسبريسو وكاكاو\", \"de\": \"Klassisches Tiramisù mit Mascarpone, Espresso & Kakaopulver\", \"en\": \"Classic Tiramisù with mascarpone, espresso & cocoa powder\", \"es\": \"Tiramisú clásico con mascarpone, espresso y cacao en polvo\", \"fr\": \"Tiramisù classique avec mascarpone, espresso et cacao\", \"hi\": \"क्लासिक तिरामिसू, मस्कारपोन, एस्प्रेसो और कोको पाउडर\", \"it\": \"Tiramisù classico con mascarpone, espresso e cacao\", \"ja\": \"クラシックティラミス、マスカルポーネ、エスプレッソ、ココアパウダー\", \"ko\": \"클래식 티라미수, 마스카포네, 에스프레소, 코코아 파우더\", \"pt\": \"Tiramisù clássico com mascarpone, espresso e cacau\", \"zh\": \"经典Tiramisù，马斯卡彭芝士、浓缩咖啡与可可粉\"}',0,0.00,0.00,0,0,0,0,0,0,0,0,23,NULL,NULL,'2026-04-14 15:39:19','2026-04-14 16:22:43',0,0),(1,NULL,'/static/uploads/products/24.jpg',NULL,'意式奶冻','{\"ar\": \"بانا كوتا\", \"de\": \"Panna Cotta\", \"en\": \"Panna Cotta\", \"es\": \"Panna Cotta\", \"fr\": \"Panna Cotta\", \"hi\": \"पन्ना कोटा\", \"it\": \"Panna Cotta\", \"ja\": \"パンナコッタ\", \"ko\": \"판나코타\", \"pt\": \"Panna Cotta\", \"zh\": \"意式奶冻\"}','Panna Cotta香草奶冻配新鲜莓果与焦糖酱','{\"ar\": \"بانا كوتا فانيليا مع توت طازج وصلصة كراميل\", \"de\": \"Vanille-Panna-Cotta mit frischen Beeren & Karamellsauce\", \"en\": \"Vanilla Panna Cotta with fresh berries & caramel sauce\", \"es\": \"Panna Cotta de vainilla con frutos rojos frescos y salsa de caramelo\", \"fr\": \"Panna Cotta vanille avec fruits rouges frais et sauce caramel\", \"hi\": \"वनीला पन्ना कोटा, ताज़े बेरीज़ और कैरामेल सॉस\", \"it\": \"Panna Cotta alla vaniglia con frutti di bosco freschi e salsa caramello\", \"ja\": \"バニラパンナコッタ、フレッシュベリー、キャラメルソース\", \"ko\": \"바닐라 판나코타, 신선한 베리, 카라멜 소스\", \"pt\": \"Panna Cotta de baunilha com frutos vermelhos frescos e calda de caramelo\", \"zh\": \"Panna Cotta香草奶冻配新鲜莓果与焦糖酱\"}',NULL,NULL,'8',NULL,38.00,0.00,45.00,0.00,'份',2,0,99,1,0,0,0,0,'Panna Cotta香草奶冻配新鲜莓果与焦糖酱','{\"ar\": \"بانا كوتا فانيليا مع توت طازج وصلصة كراميل\", \"de\": \"Vanille-Panna-Cotta mit frischen Beeren & Karamellsauce\", \"en\": \"Vanilla Panna Cotta with fresh berries & caramel sauce\", \"es\": \"Panna Cotta de vainilla con frutos rojos frescos y salsa de caramelo\", \"fr\": \"Panna Cotta vanille avec fruits rouges frais et sauce caramel\", \"hi\": \"वनीला पन्ना कोटा, ताज़े बेरीज़ और कैरामेल सॉस\", \"it\": \"Panna Cotta alla vaniglia con frutti di bosco freschi e salsa caramello\", \"ja\": \"バニラパンナコッタ、フレッシュベリー、キャラメルソース\", \"ko\": \"바닐라 판나코타, 신선한 베리, 카라멜 소스\", \"pt\": \"Panna Cotta de baunilha com frutos vermelhos frescos e calda de caramelo\", \"zh\": \"Panna Cotta香草奶冻配新鲜莓果与焦糖酱\"}',0,0.00,0.00,0,0,1,0,0,0,0,0,24,NULL,NULL,'2026-04-14 15:39:19','2026-04-15 01:35:45',0,0),(1,NULL,'/static/uploads/products/25.jpg',NULL,'巧克力熔岩蛋糕','{\"ar\": \"كيك لافا شوكولاتة\", \"de\": \"Schokoladen-Lavakuchen\", \"en\": \"Chocolate Lava Cake\", \"es\": \"Volcán de Chocolate\", \"fr\": \"Fondant au Chocolat\", \"hi\": \"चॉकलेट लावा केक\", \"it\": \"Tortino al Cioccolato\", \"ja\": \"チョコレートラバケーキ\", \"ko\": \"초콜릿 라바 케이크\", \"pt\": \"Petit Gâteau de Chocolate\", \"zh\": \"巧克力熔岩蛋糕\"}','法芙娜巧克力制作，切开流心，配香草冰淇淋','{\"ar\": \"شوكولاتة فالرونا، قلب سائل، مع آيس كريم فانيليا\", \"de\": \"Aus Valrhona-Schokolade, flüssiger Kern, mit Vanilleeis\", \"en\": \"Made with Valrhona chocolate, molten center, served with vanilla ice cream\", \"es\": \"Elaborado con chocolate Valrhona, centro fundido, con helado de vainilla\", \"fr\": \"Chocolat Valrhona, cœur coulant, servi avec glace vanille\", \"hi\": \"वैलरोना चॉकलेट, पिघला हुआ केंद्र, वनीला आइसक्रीम\", \"it\": \"Cioccolato Valrhona, cuore fondente, servito con gelato alla vaniglia\", \"ja\": \"ヴァローナチョコレート使用、溶岩のような中心、バニラアイス添え\", \"ko\": \"발로나 초콜릿, 용암처럼 흐르는 속, 바닐라 아이스크림 곁들임\", \"pt\": \"Chocolate Valrhona, centro derretido, servido com sorvete de baunilha\", \"zh\": \"法芙娜巧克力制作，切开流心，配香草冰淇淋\"}',NULL,NULL,'8',NULL,48.00,0.00,56.00,0.00,'份',3,1,98,1,0,0,0,0,'法芙娜巧克力制作，切开流心，配香草冰淇淋','{\"ar\": \"شوكولاتة فالرونا، قلب سائل، مع آيس كريم فانيليا\", \"de\": \"Aus Valrhona-Schokolade, flüssiger Kern, mit Vanilleeis\", \"en\": \"Made with Valrhona chocolate, molten center, served with vanilla ice cream\", \"es\": \"Elaborado con chocolate Valrhona, centro fundido, con helado de vainilla\", \"fr\": \"Chocolat Valrhona, cœur coulant, servi avec glace vanille\", \"hi\": \"वैलरोना चॉकलेट, पिघला हुआ केंद्र, वनीला आइसक्रीम\", \"it\": \"Cioccolato Valrhona, cuore fondente, servito con gelato alla vaniglia\", \"ja\": \"ヴァローナチョコレート使用、溶岩のような中心、バニラアイス添え\", \"ko\": \"발로나 초콜릿, 용암처럼 흐르는 속, 바닐라 아이스크림 곁들임\", \"pt\": \"Chocolate Valrhona, centro derretido, servido com sorvete de baunilha\", \"zh\": \"法芙娜巧克力制作，切开流心，配香草冰淇淋\"}',0,0.00,0.00,0,0,0,0,0,0,0,0,25,NULL,NULL,'2026-04-14 15:39:19','2026-04-14 16:22:43',0,0),(1,NULL,'/static/uploads/products/26.jpg',NULL,'柠檬塔','{\"ar\": \"تارت ليمون\", \"de\": \"Zitronentarte\", \"en\": \"Lemon Tart\", \"es\": \"Tarta de Limón\", \"fr\": \"Tarte au Citron\", \"hi\": \"लेमन टार्ट\", \"it\": \"Crostata al Limone\", \"ja\": \"レモンタルト\", \"ko\": \"레몬 타르트\", \"pt\": \"Torta de Limão\", \"zh\": \"柠檬塔\"}','西西里柠檬塔配烤蛋白霜与柠檬皮屑','{\"ar\": \"تارت ليمون صقلي مع ميرانغ محمص وقشر ليمون\", \"de\": \"Sizilianische Zitronentarte mit geflammter Meringue & Zitronenzeste\", \"en\": \"Sicilian lemon tart with torched meringue & lemon zest\", \"es\": \"Tarta de limón siciliana con merengue flambeado y ralladura de limón\", \"fr\": \"Tarte au citron sicilien avec meringue flambée et zeste de citron\", \"hi\": \"सिसिलियन लेमन टार्ट, टॉर्च्ड मेरिंग और लेमन ज़ेस्ट\", \"it\": \"Crostata al limone siciliano con meringa fiammeggiata e scorza di limone\", \"ja\": \"シチリアレモンタルト、炙りメレンゲ、レモンゼスト\", \"ko\": \"시칠리아 레몬 타르트, 토치 머랭, 레몬 제스트\", \"pt\": \"Torta de limão siciliano com merengue maçaricado e raspas de limão\", \"zh\": \"西西里柠檬塔配烤蛋白霜与柠檬皮屑\"}',NULL,NULL,'8',NULL,36.00,0.00,42.00,0.00,'份',4,0,99,1,0,0,0,0,'西西里柠檬塔配烤蛋白霜与柠檬皮屑','{\"ar\": \"تارت ليمون صقلي مع ميرانغ محمص وقشر ليمون\", \"de\": \"Sizilianische Zitronentarte mit geflammter Meringue & Zitronenzeste\", \"en\": \"Sicilian lemon tart with torched meringue & lemon zest\", \"es\": \"Tarta de limón siciliana con merengue flambeado y ralladura de limón\", \"fr\": \"Tarte au citron sicilien avec meringue flambée et zeste de citron\", \"hi\": \"सिसिलियन लेमन टार्ट, टॉर्च्ड मेरिंग और लेमन ज़ेस्ट\", \"it\": \"Crostata al limone siciliano con meringa fiammeggiata e scorza di limone\", \"ja\": \"シチリアレモンタルト、炙りメレンゲ、レモンゼスト\", \"ko\": \"시칠리아 레몬 타르트, 토치 머랭, 레몬 제스트\", \"pt\": \"Torta de limão siciliano com merengue maçaricado e raspas de limão\", \"zh\": \"西西里柠檬塔配烤蛋白霜与柠檬皮屑\"}',0,0.00,0.00,0,0,1,0,0,0,0,0,26,NULL,NULL,'2026-04-14 15:39:19','2026-04-15 15:14:12',0,0),(1,NULL,'/static/uploads/products/27.jpg',NULL,'意式浓缩咖啡','{\"ar\": \"إسبريسو\", \"de\": \"Espresso\", \"en\": \"Espresso\", \"es\": \"Espresso\", \"fr\": \"Espresso\", \"hi\": \"एस्प्रेसो\", \"it\": \"Espresso\", \"ja\": \"エスプレッソ\", \"ko\": \"에스프레소\", \"pt\": \"Espresso\", \"zh\": \"意式浓缩咖啡\"}','Espresso双份浓缩，精选意大利烘焙咖啡豆','{\"ar\": \"إسبريسو مزدوج، حبوب محمصة إيطالية مختارة\", \"de\": \"Doppelter Espresso, ausgewählte italienische Röstung\", \"en\": \"Double shot espresso, select Italian roasted beans\", \"es\": \"Espresso doble, granos tostados italianos selectos\", \"fr\": \"Double espresso, grains torréfiés italiens sélectionnés\", \"hi\": \"डबल शॉट एस्प्रेसो, चुनिंदा इटालियन रोस्ट बीन्स\", \"it\": \"Doppio espresso, chicchi di caffè tostati italiani selezionati\", \"ja\": \"ダブルショットエスプレッソ、厳選イタリアンロースト豆\", \"ko\": \"더블 에스프레소, 엄선된 이탈리안 로스팅 원두\", \"pt\": \"Espresso duplo, grãos torrados italianos selecionados\", \"zh\": \"Espresso双份浓缩，精选意大利烘焙咖啡豆\"}',NULL,NULL,'9',NULL,28.00,0.00,32.00,0.00,'杯',1,1,98,1,0,0,0,0,'Espresso双份浓缩，精选意大利烘焙咖啡豆','{\"ar\": \"إسبريسو مزدوج، حبوب محمصة إيطالية مختارة\", \"de\": \"Doppelter Espresso, ausgewählte italienische Röstung\", \"en\": \"Double shot espresso, select Italian roasted beans\", \"es\": \"Espresso doble, granos tostados italianos selectos\", \"fr\": \"Double espresso, grains torréfiés italiens sélectionnés\", \"hi\": \"डबल शॉट एस्प्रेसो, चुनिंदा इटालियन रोस्ट बीन्स\", \"it\": \"Doppio espresso, chicchi di caffè tostati italiani selezionati\", \"ja\": \"ダブルショットエスプレッソ、厳選イタリアンロースト豆\", \"ko\": \"더블 에스프레소, 엄선된 이탈리안 로스팅 원두\", \"pt\": \"Espresso duplo, grãos torrados italianos selecionados\", \"zh\": \"Espresso双份浓缩，精选意大利烘焙咖啡豆\"}',0,0.00,0.00,0,0,1,0,0,0,0,0,27,NULL,NULL,'2026-04-14 15:39:51','2026-04-15 15:14:10',0,0),(1,NULL,'/static/uploads/products/28.jpg',NULL,'卡布奇诺','{\"ar\": \"كابتشينو\", \"de\": \"Cappuccino\", \"en\": \"Cappuccino\", \"es\": \"Capuchino\", \"fr\": \"Cappuccino\", \"hi\": \"कैपुचीनो\", \"it\": \"Cappuccino\", \"ja\": \"カプチーノ\", \"ko\": \"카푸치노\", \"pt\": \"Cappuccino\", \"zh\": \"卡布奇诺\"}','经典Cappuccino，绵密奶泡配可可粉拉花','{\"ar\": \"كابتشينو كلاسيكي مع رغوة حريرية وكاكاو\", \"de\": \"Klassischer Cappuccino mit samtiger Milchschaum & Kakaopulver\", \"en\": \"Classic Cappuccino with silky foam & cocoa dusting\", \"es\": \"Capuchino clásico con espuma sedosa y cacao espolvoreado\", \"fr\": \"Cappuccino classique avec mousse soyeuse et cacao\", \"hi\": \"क्लासिक कैपुचीनो, सिल्की फोम और कोको पाउडर\", \"it\": \"Cappuccino classico con schiuma vellutata e cacao\", \"ja\": \"クラシックカプチーノ、シルキーフォーム、ココアパウダー\", \"ko\": \"클래식 카푸치노, 실키한 거품, 코코아 파우더\", \"pt\": \"Cappuccino clássico com espuma sedosa e cacau\", \"zh\": \"经典Cappuccino，绵密奶泡配可可粉拉花\"}',NULL,NULL,'9',NULL,32.00,0.00,38.00,0.00,'杯',2,2,97,1,0,0,0,0,'经典Cappuccino，绵密奶泡配可可粉拉花','{\"ar\": \"كابتشينو كلاسيكي مع رغوة حريرية وكاكاو\", \"de\": \"Klassischer Cappuccino mit samtiger Milchschaum & Kakaopulver\", \"en\": \"Classic Cappuccino with silky foam & cocoa dusting\", \"es\": \"Capuchino clásico con espuma sedosa y cacao espolvoreado\", \"fr\": \"Cappuccino classique avec mousse soyeuse et cacao\", \"hi\": \"क्लासिक कैपुचीनो, सिल्की फोम और कोको पाउडर\", \"it\": \"Cappuccino classico con schiuma vellutata e cacao\", \"ja\": \"クラシックカプチーノ、シルキーフォーム、ココアパウダー\", \"ko\": \"클래식 카푸치노, 실키한 거품, 코코아 파우더\", \"pt\": \"Cappuccino clássico com espuma sedosa e cacau\", \"zh\": \"经典Cappuccino，绵密奶泡配可可粉拉花\"}',0,0.00,0.00,0,0,3,0,0,0,0,0,28,NULL,NULL,'2026-04-14 15:39:51','2026-04-15 15:12:37',0,0),(1,NULL,'/static/uploads/products/29.jpg',NULL,'柠檬气泡水','{\"ar\": \"مياه غازية بالليمون\", \"de\": \"Zitronen-Sprudelwasser\", \"en\": \"Lemon Sparkling Water\", \"es\": \"Agua con Gas y Limón\", \"fr\": \"Eau Pétillante Citron\", \"hi\": \"लेमन स्पार्कलिंग वॉटर\", \"it\": \"Acqua Frizzante al Limone\", \"ja\": \"レモンスパークリングウォーター\", \"ko\": \"레몬 탄산수\", \"pt\": \"Água com Gás e Limão\", \"zh\": \"柠檬气泡水\"}','San Pellegrino气泡水配新鲜柠檬与薄荷','{\"ar\": \"سان بيليغرينو مع ليمون طازج ونعناع\", \"de\": \"San Pellegrino Sprudelwasser mit frischer Zitrone & Minze\", \"en\": \"San Pellegrino sparkling water with fresh lemon & mint\", \"es\": \"Agua con gas San Pellegrino con limón fresco y menta\", \"fr\": \"San Pellegrino avec citron frais et menthe\", \"hi\": \"सैन पेलेग्रिनो स्पार्कलिंग वॉटर, ताज़ा नींबू और पुदीना\", \"it\": \"San Pellegrino con limone fresco e menta\", \"ja\": \"サンペレグリノ炭酸水、フレッシュレモン＆ミント\", \"ko\": \"산 펠레그리노 탄산수, 신선한 레몬과 민트\", \"pt\": \"San Pellegrino com limão fresco e hortelã\", \"zh\": \"San Pellegrino气泡水配新鲜柠檬与薄荷\"}',NULL,NULL,'9',NULL,22.00,0.00,28.00,0.00,'杯',3,1,98,1,0,0,0,0,'San Pellegrino气泡水配新鲜柠檬与薄荷','{\"ar\": \"سان بيليغرينو مع ليمون طازج ونعناع\", \"de\": \"San Pellegrino Sprudelwasser mit frischer Zitrone & Minze\", \"en\": \"San Pellegrino sparkling water with fresh lemon & mint\", \"es\": \"Agua con gas San Pellegrino con limón fresco y menta\", \"fr\": \"San Pellegrino avec citron frais et menthe\", \"hi\": \"सैन पेलेग्रिनो स्पार्कलिंग वॉटर, ताज़ा नींबू और पुदीना\", \"it\": \"San Pellegrino con limone fresco e menta\", \"ja\": \"サンペレグリノ炭酸水、フレッシュレモン＆ミント\", \"ko\": \"산 펠레그리노 탄산수, 신선한 레몬과 민트\", \"pt\": \"San Pellegrino com limão fresco e hortelã\", \"zh\": \"San Pellegrino气泡水配新鲜柠檬与薄荷\"}',0,0.00,0.00,0,0,0,0,0,0,0,0,29,NULL,NULL,'2026-04-14 15:39:51','2026-04-14 16:22:43',0,0),(1,NULL,'/static/uploads/products/30.jpg',NULL,'Aperol Spritz','{\"ar\": \"أبيرول سبريتز\", \"de\": \"Aperol Spritz\", \"en\": \"Aperol Spritz\", \"es\": \"Aperol Spritz\", \"fr\": \"Aperol Spritz\", \"hi\": \"एपेरोल स्प्रिट्ज़\", \"it\": \"Aperol Spritz\", \"ja\": \"アペロールスプリッツ\", \"ko\": \"아페롤 스프리츠\", \"pt\": \"Aperol Spritz\", \"zh\": \"Aperol Spritz\"}','经典意大利开胃酒，Aperol、Prosecco与苏打水','{\"ar\": \"مشروب إيطالي كلاسيكي: أبيرول وبروسيكو وصودا\", \"de\": \"Klassischer italienischer Aperitif: Aperol, Prosecco & Soda\", \"en\": \"Classic Italian aperitif: Aperol, Prosecco & soda\", \"es\": \"Aperitivo italiano clásico: Aperol, Prosecco y soda\", \"fr\": \"Apéritif italien classique: Aperol, Prosecco et soda\", \"hi\": \"क्लासिक इटालियन एपेरिटिफ: एपेरोल, प्रोसेको और सोडा\", \"it\": \"Classico aperitivo italiano: Aperol, Prosecco e soda\", \"ja\": \"クラシックイタリアンアペリティフ：アペロール、プロセッコ、ソーダ\", \"ko\": \"클래식 이탈리안 아페리티프: 아페롤, 프로세코, 소다\", \"pt\": \"Aperitivo italiano clássico: Aperol, Prosecco e soda\", \"zh\": \"经典意大利开胃酒，Aperol、Prosecco与苏打水\"}',NULL,NULL,'9',NULL,52.00,0.00,62.00,0.00,'杯',4,2,97,1,0,0,0,0,'经典意大利开胃酒，Aperol、Prosecco与苏打水','{\"ar\": \"مشروب إيطالي كلاسيكي: أبيرول وبروسيكو وصودا\", \"de\": \"Klassischer italienischer Aperitif: Aperol, Prosecco & Soda\", \"en\": \"Classic Italian aperitif: Aperol, Prosecco & soda\", \"es\": \"Aperitivo italiano clásico: Aperol, Prosecco y soda\", \"fr\": \"Apéritif italien classique: Aperol, Prosecco et soda\", \"hi\": \"क्लासिक इटालियन एपेरिटिफ: एपेरोल, प्रोसेको और सोडा\", \"it\": \"Classico aperitivo italiano: Aperol, Prosecco e soda\", \"ja\": \"クラシックイタリアンアペリティフ：アペロール、プロセッコ、ソーダ\", \"ko\": \"클래식 이탈리안 아페리티프: 아페롤, 프로세코, 소다\", \"pt\": \"Aperitivo italiano clássico: Aperol, Prosecco e soda\", \"zh\": \"经典意大利开胃酒，Aperol、Prosecco与苏打水\"}',0,0.00,0.00,0,0,2,0,0,0,0,0,30,NULL,NULL,'2026-04-14 15:39:51','2026-04-15 15:12:37',0,0),(1,NULL,'/static/uploads/products/31.jpg',NULL,'红酒（杯）','{\"ar\": \"نبيذ أحمر (كأس)\", \"de\": \"Rotwein (Glas)\", \"en\": \"Red Wine (Glass)\", \"es\": \"Vino tinto (copa)\", \"fr\": \"Vin rouge (verre)\", \"hi\": \"रेड वाइन (ग्लास)\", \"it\": \"Vino rosso (bicchiere)\", \"ja\": \"赤ワイン（グラス）\", \"ko\": \"레드 와인 (글라스)\", \"pt\": \"Vinho tinto (taça)\", \"zh\": \"红酒（杯）\"}','精选意大利红葡萄酒，单杯供应','{\"ar\": \"نبيذ أحمر إيطالي مختار، يقدم بالكأس\", \"de\": \"Ausgewählter italienischer Rotwein, glasweise serviert\", \"en\": \"Select Italian red wine, served by the glass\", \"es\": \"Vino tinto italiano selecto, servido por copa\", \"fr\": \"Vin rouge italien sélectionné, servi au verre\", \"hi\": \"चुनिंदा इटालियन रेड वाइन, ग्लास में परोसा\", \"it\": \"Vino rosso italiano selezionato, servito al bicchiere\", \"ja\": \"厳選イタリア赤ワイン、グラス提供\", \"ko\": \"엄선된 이탈리아 레드 와인, 글라스 제공\", \"pt\": \"Vinho tinto italiano selecionado, servido em taça\", \"zh\": \"精选意大利红葡萄酒，单杯供应\"}',NULL,NULL,NULL,NULL,58.00,0.00,0.00,0.00,NULL,5,1,98,1,0,0,0,0,'精选意大利红葡萄酒，单杯供应','{\"ar\": \"نبيذ أحمر إيطالي مختار، يقدم بالكأس\", \"de\": \"Ausgewählter italienischer Rotwein, glasweise serviert\", \"en\": \"Select Italian red wine, served by the glass\", \"es\": \"Vino tinto italiano selecto, servido por copa\", \"fr\": \"Vin rouge italien sélectionné, servi au verre\", \"hi\": \"चुनिंदा इटालियन रेड वाइन, ग्लास में परोसा\", \"it\": \"Vino rosso italiano selezionato, servito al bicchiere\", \"ja\": \"厳選イタリア赤ワイン、グラス提供\", \"ko\": \"엄선된 이탈리아 레드 와인, 글라스 제공\", \"pt\": \"Vinho tinto italiano selecionado, servido em taça\", \"zh\": \"精选意大利红葡萄酒，单杯供应\"}',0,0.00,0.00,0,0,9,0,0,0,0,0,31,NULL,NULL,'2026-04-14 15:39:51','2026-04-15 15:23:29',0,0),(1,NULL,'',NULL,'白葡萄酒（杯）','{\"ar\": \"نبيذ أبيض (كأس)\", \"de\": \"Weißwein (Glas)\", \"en\": \"White Wine (Glass)\", \"es\": \"Vino Blanco (Copa)\", \"fr\": \"Vin Blanc (Verre)\", \"hi\": \"व्हाइट वाइन (ग्लास)\", \"it\": \"Vino Bianco (Calice)\", \"ja\": \"白ワイン（グラス）\", \"ko\": \"화이트 와인 (잔)\", \"pt\": \"Vinho Branco (Copo)\", \"zh\": \"白葡萄酒（杯）\"}','精选意大利白葡萄酒，单杯供应','{\"ar\": \"نبيذ أبيض إيطالي مختار، يقدم بالكأس\", \"de\": \"Ausgewählter italienischer Weißwein, glasweise serviert\", \"en\": \"Select Italian white wine, served by the glass\", \"es\": \"Vino blanco italiano selecto, servido por copa\", \"fr\": \"Vin blanc italien sélectionné, servi au verre\", \"hi\": \"चुनिंदा इटालियन व्हाइट वाइन, ग्लास में परोसा\", \"it\": \"Vino bianco italiano selezionato, servito al bicchiere\", \"ja\": \"厳選イタリア白ワイン、グラス提供\", \"ko\": \"엄선된 이탈리아 화이트 와인, 글라스 제공\", \"pt\": \"Vinho branco italiano selecionado, servido em taça\", \"zh\": \"精选意大利白葡萄酒，单杯供应\"}',NULL,NULL,NULL,NULL,42.00,0.00,0.00,0.00,NULL,0,1,99,1,0,0,0,0,'精选意大利白葡萄酒，单杯供应','{\"ar\": \"نبيذ أبيض إيطالي مختار، يقدم بالكأس\", \"de\": \"Ausgewählter italienischer Weißwein, glasweise serviert\", \"en\": \"Select Italian white wine, served by the glass\", \"es\": \"Vino blanco italiano selecto, servido por copa\", \"fr\": \"Vin blanc italien sélectionné, servi au verre\", \"hi\": \"चुनिंदा इटालियन व्हाइट वाइन, ग्लास में परोसा\", \"it\": \"Vino bianco italiano selezionato, servito al bicchiere\", \"ja\": \"厳選イタリア白ワイン、グラス提供\", \"ko\": \"엄선된 이탈리아 화이트 와인, 글라스 제공\", \"pt\": \"Vinho branco italiano selecionado, servido em taça\", \"zh\": \"精选意大利白葡萄酒，单杯供应\"}',0,0.00,0.00,0,0,1,0,0,0,0,0,32,NULL,NULL,'2026-04-14 15:39:51','2026-04-15 01:37:06',0,0),(1,NULL,'',NULL,'测试菜品',NULL,NULL,NULL,NULL,NULL,'1',NULL,10.00,0.00,0.00,0.00,NULL,0,0,50,1,0,0,0,0,'',NULL,0,0.00,0.00,0,0,0,0,0,0,0,0,33,NULL,NULL,'2026-04-14 20:24:49','2026-04-14 20:24:56',1,0);
/*!40000 ALTER TABLE `go2run_store_product` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `go2run_store_product_category` WRITE;
/*!40000 ALTER TABLE `go2run_store_product_category` DISABLE KEYS */;
INSERT INTO `go2run_store_product_category` (`shop_id`, `shop_name`, `parent_id`, `name`, `name_i18n`, `pic_url`, `sort`, `description`, `status`, `id`, `creator`, `updater`, `create_time`, `update_time`, `deleted`, `tenant_id`) VALUES (1,NULL,0,'🥗 开胃菜','{\"ar\": \"🥗 مقبلات\", \"de\": \"🥗 Vorspeisen\", \"en\": \"🥗 Antipasti\", \"es\": \"🥗 Entrantes\", \"fr\": \"🥗 Entrées\", \"hi\": \"🥗 ऐपेटाइज़र\", \"it\": \"🥗 Antipasti\", \"ja\": \"🥗 前菜\", \"ko\": \"🥗 전채요리\", \"pt\": \"🥗 Entradas\", \"zh\": \"🥗 开胃菜\"}','/static/uploads/categories/4.jpg',1,NULL,0,4,NULL,NULL,'2026-04-14 15:37:57','2026-04-14 15:37:57',0,0),(1,NULL,0,'🍝 意面','{\"ar\": \"🍝 معكرونة\", \"de\": \"🍝 Pasta\", \"en\": \"🍝 Pasta\", \"es\": \"🍝 Pasta\", \"fr\": \"🍝 Pâtes\", \"hi\": \"🍝 पास्ता\", \"it\": \"🍝 Pasta\", \"ja\": \"🍝 パスタ\", \"ko\": \"🍝 파스타\", \"pt\": \"🍝 Massa\", \"zh\": \"🍝 意面\"}','/static/uploads/categories/5.jpg',2,NULL,0,5,NULL,NULL,'2026-04-14 15:37:57','2026-04-14 15:37:57',0,0),(1,NULL,0,'🍕 披萨','{\"ar\": \"🍕 بيتزا\", \"de\": \"🍕 Pizza\", \"en\": \"🍕 Pizza\", \"es\": \"🍕 Pizza\", \"fr\": \"🍕 Pizza\", \"hi\": \"🍕 पिज़्ज़ा\", \"it\": \"🍕 Pizza\", \"ja\": \"🍕 ピザ\", \"ko\": \"🍕 피자\", \"pt\": \"🍕 Pizza\", \"zh\": \"🍕 披萨\"}','/static/uploads/categories/6.jpg',3,NULL,0,6,NULL,NULL,'2026-04-14 15:37:57','2026-04-14 15:37:57',0,0),(1,NULL,0,'🥩 主菜','{\"ar\": \"🥩 الأطباق الرئيسية\", \"de\": \"🥩 Hauptgerichte\", \"en\": \"🥩 Secondi\", \"es\": \"🥩 Segundos\", \"fr\": \"🥩 Plats principaux\", \"hi\": \"🥩 मुख्य व्यंजन\", \"it\": \"🥩 Secondi\", \"ja\": \"🥩 メイン\", \"ko\": \"🥩 메인요리\", \"pt\": \"🥩 Pratos principais\", \"zh\": \"🥩 主菜\"}','/static/uploads/categories/7.jpg',4,NULL,0,7,NULL,NULL,'2026-04-14 15:37:57','2026-04-14 15:37:57',0,0),(1,NULL,0,'🍰 甜点','{\"ar\": \"🍰 حلويات\", \"de\": \"🍰 Desserts\", \"en\": \"🍰 Dolci\", \"es\": \"🍰 Postres\", \"fr\": \"🍰 Desserts\", \"hi\": \"🍰 मिठाई\", \"it\": \"🍰 Dolci\", \"ja\": \"🍰 デザート\", \"ko\": \"🍰 디저트\", \"pt\": \"🍰 Sobremesas\", \"zh\": \"🍰 甜点\"}','/static/uploads/categories/8.jpg',5,NULL,0,8,NULL,NULL,'2026-04-14 15:37:57','2026-04-15 01:36:43',0,0),(1,NULL,0,'🥂 饮品','{\"ar\": \"🥂 مشروبات\", \"de\": \"🥂 Getränke\", \"en\": \"🥂 Bevande\", \"es\": \"🥂 Bebidas\", \"fr\": \"🥂 Boissons\", \"hi\": \"🥂 पेय\", \"it\": \"🥂 Bevande\", \"ja\": \"🥂 ドリンク\", \"ko\": \"🥂 음료\", \"pt\": \"🥂 Bebidas\", \"zh\": \"🥂 饮品\"}','/static/uploads/06864bfa1f53.png',6,NULL,0,9,NULL,NULL,'2026-04-14 15:37:57','2026-04-15 01:33:14',0,0);
/*!40000 ALTER TABLE `go2run_store_product_category` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `go2run_store_product_attr` WRITE;
/*!40000 ALTER TABLE `go2run_store_product_attr` DISABLE KEYS */;
/*!40000 ALTER TABLE `go2run_store_product_attr` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `go2run_store_product_attr_value` WRITE;
/*!40000 ALTER TABLE `go2run_store_product_attr_value` DISABLE KEYS */;
/*!40000 ALTER TABLE `go2run_store_product_attr_value` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `go2run_store_product_attr_result` WRITE;
/*!40000 ALTER TABLE `go2run_store_product_attr_result` DISABLE KEYS */;
INSERT INTO `go2run_store_product_attr_result` (`id`, `product_id`, `result`, `change_time`) VALUES (1,6,'{}',NULL),(2,7,'{}',NULL),(3,8,'{}',NULL),(4,9,'{}',NULL),(5,10,'{}',NULL),(6,11,'{}',NULL),(7,12,'{}',NULL),(8,13,'{}',NULL),(9,14,'{}',NULL),(10,15,'{}',NULL),(11,16,'{}',NULL),(12,17,'{}',NULL),(13,18,'{}',NULL),(14,19,'{}',NULL),(15,20,'{}',NULL),(16,21,'{}',NULL),(17,22,'{}',NULL),(18,23,'{}',NULL),(19,24,'{}',NULL),(20,25,'{}',NULL),(21,26,'{}',NULL),(22,27,'{}',NULL),(23,28,'{}',NULL),(24,29,'{}',NULL),(25,30,'{}',NULL),(26,31,'{}',NULL),(27,32,'{}',NULL),(28,33,'{}',NULL);
/*!40000 ALTER TABLE `go2run_store_product_attr_result` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `go2run_store_product_rule` WRITE;
/*!40000 ALTER TABLE `go2run_store_product_rule` DISABLE KEYS */;
/*!40000 ALTER TABLE `go2run_store_product_rule` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `go2run_store_table` WRITE;
/*!40000 ALTER TABLE `go2run_store_table` DISABLE KEYS */;
INSERT INTO `go2run_store_table` (`id`, `shop_id`, `table_no`, `area`, `seats`, `status`, `qr_url`, `creator`, `updater`, `create_time`, `update_time`, `deleted`, `tenant_id`, `last_settled_at`) VALUES (1,1,'A1','大厅',4,1,NULL,NULL,NULL,'2026-04-14 12:55:02','2026-04-14 15:37:38',0,0,NULL),(2,1,'B2','包间',4,1,NULL,NULL,NULL,'2026-04-14 16:22:12','2026-04-14 16:23:14',0,0,'2026-04-14 16:23:15');
/*!40000 ALTER TABLE `go2run_store_table` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `system_users` WRITE;
/*!40000 ALTER TABLE `system_users` DISABLE KEYS */;
INSERT INTO `system_users` (`username`, `password`, `nickname`, `remark`, `dept_id`, `post_ids`, `email`, `mobile`, `sex`, `avatar`, `status`, `login_ip`, `login_date`, `id`, `creator`, `updater`, `create_time`, `update_time`, `deleted`, `tenant_id`) VALUES ('admin','$2b$12$WZOKpVtqJpUhYeo9M2gAmObhLDl0hGdShcuRMVxnxQt/J5JY.lgqe','超级管理员',NULL,NULL,NULL,NULL,NULL,0,NULL,0,NULL,'2026-04-14 12:37:46',1,NULL,NULL,'2026-04-13 21:02:41','2026-04-14 20:37:46',0,0);
/*!40000 ALTER TABLE `system_users` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `system_role` WRITE;
/*!40000 ALTER TABLE `system_role` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_role` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `system_menu` WRITE;
/*!40000 ALTER TABLE `system_menu` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_menu` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `system_dept` WRITE;
/*!40000 ALTER TABLE `system_dept` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_dept` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

