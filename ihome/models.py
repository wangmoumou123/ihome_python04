# -*- coding:utf-8 -*-

from datetime import datetime
from . import db
from ihome import constants

from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""

    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


class User(BaseModel, db.Model):
    """用户"""

    __tablename__ = "ih_user_profile"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    real_name = db.Column(db.String(32))  # 真实姓名
    id_card = db.Column(db.String(20))  # 身份证号
    avatar_url = db.Column(db.String(128))  # 用户头像路径
    houses = db.relationship("House", backref="user")  # 用户发布的房屋
    orders = db.relationship("Order", backref="user")  # 用户下的订单

    # 定义property,并且是只能设置不能读取
    @property
    def password(self):
        """
        用读取实力属性的方法读取实例方法
        :return:
        """
        raise AttributeError('只能设置， 不能读取')

    # 设置sha256加密
    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, origin_password):
        """
        密码校验
        :param origin_password:
        :return:
        """
        return check_password_hash(self.password_hash, origin_password)


class Area(BaseModel, db.Model):
    """城区"""

    __tablename__ = "ih_area_info"

    id = db.Column(db.Integer, primary_key=True)  # 区域编号
    name = db.Column(db.String(32), nullable=False)  # 区域名字
    houses = db.relationship("House", backref="area")  # 区域的房屋

    def to_dict(self):
        """
        转换为字典
        :return:
        """
        _dict = {'aid': self.id,
                 'aname': self.name}
        return _dict

    # 房屋设施表，建立房屋与设施的多对多关系


house_facility = db.Table(
    "ih_house_facility",
    db.Column("house_id", db.Integer, db.ForeignKey("ih_house_info.id"), primary_key=True),  # 房屋编号
    db.Column("facility_id", db.Integer, db.ForeignKey("ih_facility_info.id"), primary_key=True)  # 设施编号
)


class House(BaseModel, db.Model):
    """房屋信息"""

    __tablename__ = "ih_house_info"

    id = db.Column(db.Integer, primary_key=True)  # 房屋编号
    user_id = db.Column(db.Integer, db.ForeignKey("ih_user_profile.id"), nullable=False)  # 房屋主人的用户编号
    area_id = db.Column(db.Integer, db.ForeignKey("ih_area_info.id"), nullable=False)  # 归属地的区域编号
    title = db.Column(db.String(64), nullable=False)  # 标题
    price = db.Column(db.Integer, default=0)  # 单价，单位：分
    address = db.Column(db.String(512), default="")  # 地址
    room_count = db.Column(db.Integer, default=1)  # 房间数目
    acreage = db.Column(db.Integer, default=0)  # 房屋面积
    unit = db.Column(db.String(32), default="")  # 房屋单元， 如几室几厅
    capacity = db.Column(db.Integer, default=1)  # 房屋容纳的人数
    beds = db.Column(db.String(64), default="")  # 房屋床铺的配置
    deposit = db.Column(db.Integer, default=0)  # 房屋押金
    min_days = db.Column(db.Integer, default=1)  # 最少入住天数
    max_days = db.Column(db.Integer, default=0)  # 最多入住天数，0表示不限制
    order_count = db.Column(db.Integer, default=0)  # 预订完成的该房屋的订单数
    index_image_url = db.Column(db.String(256), default="")  # 房屋主图片的路径
    facilities = db.relationship("Facility", secondary=house_facility)  # 房屋的设施
    images = db.relationship("HouseImage")  # 房屋的图片
    orders = db.relationship("Order", backref="house")  # 房屋的订单

    # to_dict
    def to_basic_dict(self):
        _dict = {
            'house_id': self.id,
            'title': self.title,
            'price': self.price,
            'area_name': self.area.name,
            'index_image_url': constants.QINIU_ADDRESS + self.index_image_url if self.index_image_url else '',
            'room_count': self.room_count,
            'order_count': self.order_count,
            'address': self.address,
            'user_avatar': constants.QINIU_ADDRESS + self.user.avatar_url,
            'ctime': self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        return _dict

    def to_full_dict(self):
        _dict = {
            'house_id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.name,
            'title': self.title,
            'price': self.price,
            'area_name': self.area.name,
            'index_image_url': constants.QINIU_ADDRESS + self.index_image_url if self.index_image_url else '',
            'room_count': self.room_count,
            'acreage': self.acreage,
            'unit': self.unit,
            'capacity': self.capacity,
            'beds': self.beds,
            'deposit': self.deposit,
            'min_days': self.min_days,
            'max_days': self.max_days,
            'order_count': self.order_count,
            'address': self.address,
            'user_avatar': constants.QINIU_ADDRESS + self.user.avatar_url,
            'ctime': self.create_time.strftime('%Y-%m-%d')
        }
        # 增加房屋图片
        image_urls_list = list()
        for image in self.images:
            image_urls_list.append(constants.QINIU_ADDRESS + image.url)
        _dict['image_urls'] = image_urls_list
        # 增加设施
        facilities_list = list()
        for facility in self.facilities:
            facilities_list.append(facility.id)
        _dict['facilities_list'] = facilities_list
        # 增加评论
        commons_list = list()

        orders = Order.query.filter(Order.house_id == self.id, Order.status == 'COMPLETE', Order.comment != None) \
            .order_by(Order.update_time.desc()).limit(constants.COMMENT_NUM)
        for order in orders:
            comment = {
                'comment': order.comment,
                'user': order.user.name if order.user.name != order.user.mobile else '匿名用户',
                'ctime': order.update_time.strftime('%Y-%m-%d %H:%M:%S')
            }
            commons_list.append(comment)
        _dict['commons_list'] = commons_list
        return _dict


class Facility(BaseModel, db.Model):
    """设施信息"""

    __tablename__ = "ih_facility_info"

    id = db.Column(db.Integer, primary_key=True)  # 设施编号
    name = db.Column(db.String(32), nullable=False)  # 设施名字


class HouseImage(BaseModel, db.Model):
    """房屋图片"""

    __tablename__ = "ih_house_image"

    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey("ih_house_info.id"), nullable=False)  # 房屋编号
    url = db.Column(db.String(256), nullable=False)  # 图片的路径


class Order(BaseModel, db.Model):
    """订单"""

    __tablename__ = "ih_order_info"

    id = db.Column(db.Integer, primary_key=True)  # 订单编号
    user_id = db.Column(db.Integer, db.ForeignKey("ih_user_profile.id"), nullable=False)  # 下订单的用户编号
    house_id = db.Column(db.Integer, db.ForeignKey("ih_house_info.id"), nullable=False)  # 预订的房间编号
    begin_date = db.Column(db.DateTime, nullable=False)  # 预订的起始时间
    end_date = db.Column(db.DateTime, nullable=False)  # 预订的结束时间
    days = db.Column(db.Integer, nullable=False)  # 预订的总天数
    house_price = db.Column(db.Integer, nullable=False)  # 房屋的单价
    amount = db.Column(db.Integer, nullable=False)  # 订单的总金额
    status = db.Column(  # 订单的状态
        db.Enum(
            "WAIT_ACCEPT",  # 待接单,
            "WAIT_PAYMENT",  # 待支付
            "PAID",  # 已支付
            "WAIT_COMMENT",  # 待评价
            "COMPLETE",  # 已完成
            "CANCELED",  # 已取消
            "REJECTED"  # 已拒单
        ),
        default="WAIT_ACCEPT", index=True)
    comment = db.Column(db.Text)  # 订单的评论信息或者拒单原因
    trade_no = db.Column(db.String(80))

    def to_dict(self):
        _dict = {
            'order_id': self.id,
            'user_id': self.user_id,
            'house_id': self.house_id,
            'begin_date': self.begin_date.strftime('%Y-%m-%d '),
            'end_date': self.end_date.strftime('%Y-%m-%d '),
            'days': self.days,
            'house_price': self.house_price,
            'amount': self.amount,
            'status': self.status,
            'image_url': constants.QINIU_ADDRESS + self.house.index_image_url if self.house.index_image_url else '',
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'comment': self.comment
        }
        return _dict
