# coding:utf-8

from . import api
from flask import jsonify, current_app, request, g, session
from ihome.models import House, HouseImage, User, Order
from ihome.utils.commons import login_required
from ihome.utils.captcha.response_code import RET
from ihome import redis_store, constants, db
from ihome.utils.image_storage import storage
from datetime import datetime
import json


# 下单接口
@api.route('/order', methods=['POST'])
@login_required
def save_order():
    # 接收参数
    user_id = g.user_id

    resp_json = request.get_json()
    if not resp_json:
        return jsonify(errno=RET.NODATA, errmsg='没有数据')
    # 取出数据
    house_id = resp_json.get('house_id')
    start_time = resp_json.get('start_time')
    end_time = resp_json.get('end_time')
    # 检验数据是否完全
    if not all([house_id, start_time, end_time]):
        return jsonify(errno=RET.PARAMERR, errmdg='参数缺失')
    # 日期检查
    # 转化时间
    try:
        start_time = datetime.strptime(start_time, '%Y-%m-%d')
        end_time = datetime.strptime(end_time, '%Y-%m-%d')
        # 开始时间不能大于结束时间
        assert start_time <= end_time
        # 入住天数
        days = (end_time - start_time).days + 1
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DATAERR, errmsg='日期参数不正确')
    # 查询房屋是否存在
    try:
        house = House.query.filter_by(id=house_id).first()
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='数据库查询错误')
    # 房子不存在
    if not house:
        return jsonify(errno=RET.DBERR, errmsg='没有查询到的房子')

    # 检验预定的是不是房主
    if house.user_id == user_id:
        return jsonify(errno=RET.REQERR, errmsg='房主不能自己预定')

    # 确保订单不冲突
    try:
        orders_num = Order.query.filter(Order.house_id == house_id, Order.begin_date <= end_time,
                                        Order.end_date >= start_time).count()
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='数据库查询错误')
    # 检验是否有订单
    if orders_num > 0:
        return jsonify(errno=RET.REQERR, errmsg='房间预订时间冲突')

    # 订单总价
    amount = house.price * days
    # 创建订单
    order = Order(
        user_id=user_id,
        house_id=house_id,
        begin_date=start_time,
        end_date=end_time,
        days=days,
        house_price=house.price,
        amount=amount
    )
    # 尝试提交订单
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as ret:
        db.session.rollback()
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='订单保存失败')
    return jsonify(errno=RET.OK, errmsg='success', data={'order_id': order.id})


# 我的订单接口
# GET: /api/v1.0/my_house?role=master
@api.route('/my_order', methods=['GET'])
@login_required
def my_order():
    # 接收参数
    user_id = g.user_id
    role = request.args.get('role')
    # 查询订单数据
    try:
        # 查看订单人的角色
        # 如果是房主查看自己房子订单
        if role == 'master':
            # 先查出自己的所有房子id
            houses = House.query.filter(House.user_id == user_id).all()
            # 把房子id放入查询条件集
            houses_li = [house.id for house in houses]
            # 从订单中查询以上房子的订单
            orders = Order.query.filter(Order.house_id.in_(houses_li)).order_by(Order.create_time.desc()).all()
        else:
            # 以客户的身份查看订单
            orders = Order.query.filter(Order.user_id == user_id).order_by(Order.create_time.desc()).all()
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='数据库查询失败')
    # 返回数据
    orders_li = list()

    if orders:
        # 将orders转化为字典列表
        for order in orders:
            orders_li.append(order.to_dict())

        return jsonify(errno=RET.OK, errmsg='success', data={'orders': orders_li})
    else:

        return jsonify(errno=RET.DBERR, errmsg='暂时没有订单')


# 接单拒单接口
# GET：/api/v1.0/reject_accept_order?
@api.route('/reject_accept_order/<int:order_id>', methods=['PUT'])
@login_required
def reject_accept_order(order_id):
    # 接收参数
    user_id = g.user_id
    # action执行的动作
    resp_json = request.get_json()
    action = resp_json.get('action')
    # 检验参数是否完全
    if action not in ['reject', 'accept']:
        return jsonify(errno=RET.DATAERR, errmsg='参数错误')
    # 检验订单是否存在合法
    try:
        order = Order.query.filter(Order.id == order_id, Order.status == "WAIT_ACCEPT").first()
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='没有查询到需要处理的订单')
    if order:
        # 检验用户是否是该房主
        try:
            house = House.query.filter(House.id == order.house_id, House.user_id == user_id).first()
        except Exception as ret:
            current_app.logger.error(ret)
            return jsonify(errno=RET.DBERR, errmsg='非房主无法接单或拒单')
        if house:
            # 是房主 订单正常 可以进行接单或者拒单
            # 接单
            if action == 'accept':
                order.status = "WAIT_PAYMENT"
            # 拒单
            elif action == 'reject':
                # 拒单原因
                reason = resp_json.get('reason')
                if not reason:
                    return jsonify(errno=RET.PARAMERR, errmsg='缺少拒单原因')
                order.status = "REJECTED"
                order.comment = reason
            # 尝试保存到数据库
            try:
                db.session.add(order)
                db.session.commit()
            except Exception as ret:
                db.session.rollback()
                current_app.logger.error(ret)
                return jsonify(errno=RET.DBERR, errmsg='数据库保存接单或拒单失败')
            # 成功
            return jsonify(errno=RET.OK, errmsg='success')
        else:
            return jsonify(errno=RET.DATAERR, errmsg='未知错误')
    else:
        return jsonify(errno=RET.DATAERR, errmsg='未知错误')


# 评论接口
# GET：/api/v1.0/comment_order?
@api.route('/comment_order/<int:order_id>', methods=['PUT'])
@login_required
def comment_order(order_id):
    # 接收对应参数
    user_id = g.user_id
    # action执行的动作
    resp_json = request.get_json()
    action = resp_json.get('action')
    # 检验参数是否完全
    if action not in ['comment']:
        return jsonify(errno=RET.DATAERR, errmsg='参数错误')
    # 检验订单是否存在合法
    try:
        order = Order.query.filter(Order.id == order_id, Order.status == "WAIT_COMMENT").first()
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='没有查询到需要评论的订单')
    if order:
        # 检验用户是否是该房主
        try:
            house = House.query.filter(House.id == order.house_id, House.user_id != user_id).first()
        except Exception as ret:
            current_app.logger.error(ret)
            return jsonify(errno=RET.DBERR, errmsg='房主无法评论')
        if house:
            # 不是房主 订单正常 可以进行评论
            if action == 'comment':
                comment = resp_json.get('comment')
                if not comment:
                    return jsonify(errno=RET.PARAMERR, errmsg='缺少评论')
                # 这只状态
                order.status = "COMPLETE"
                # 设置评论
                order.comment = comment
                # 设置订单数目加1
                house.order_count += 1

            # 尝试保存到数据库
            try:
                db.session.add(house)
                db.session.add(order)
                db.session.commit()
            except Exception as ret:
                db.session.rollback()
                current_app.logger.error(ret)
                return jsonify(errno=RET.DBERR, errmsg='数据库评论失败')
            # 成功
            return jsonify(errno=RET.OK, errmsg='success_comment')
        else:
            return jsonify(errno=RET.DATAERR, errmsg='未知错误')
    else:
        return jsonify(errno=RET.DATAERR, errmsg='未知错误')
