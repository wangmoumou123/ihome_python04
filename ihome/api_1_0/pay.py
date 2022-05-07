# coding:utf-8

from . import api
from alipay import AliPay
from flask import current_app, g, jsonify, request
from ihome.utils.commons import login_required
from ihome.models import Order
from ihome.utils.captcha.response_code import RET
from ihome import constants, db
import os


# 订单支付接口
@api.route('/order_pay/<int:order_id>', methods=['POST'])
@login_required
def order_pay(order_id):
    # 取出参数
    user_id = g.user_id
    # 检验订单是否存在
    # 判断订单是否存在
    try:
        order = Order.query.filter(Order.user_id == user_id, Order.id == order_id,
                                   Order.status == 'WAIT_PAYMENT').first()
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='数据库错误')
    # 若是没有订单
    if not order:
        return jsonify(errno=RET.DATAERR, errmsg='没有查询到订单')

    # 订单存在，进一步处理支付

    # 初始化
    alipay = AliPay(
        appid="2016102300746946",
        app_notify_url=None,  # 默认回调url:
        app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem"),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/alipay_public_key.pem"),
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True,  # 默认False
    )

    # 手机网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order.id,
        total_amount=str(order.amount / 100.0),
        subject=u"开房支出%s" % order.id,
        return_url=constants.MY_APP_ADDRESS,
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    order_pay_url = constants.ALIPAY_ADDRESS + order_string

    # 返回值
    return jsonify(errno=RET.OK, errmsg='success', data={'order_pay_url': order_pay_url})


# http://127.0.0.1:5000/orders.html?charset=utf-8&out_trade_no=20&method=alipay.trade.wap.pay.return&
# total_amount=11.00&
# sign=cepuWE%2FOD53vhDJQHa0ROS3wUTee3SQYhnkkdKvsiqKi942RtfmQG1B5RAHok%2BYylNzuusD84d0pTcGznFKNXRzlr8VOEBDHNJ5KwDpnVQ92LFhxd0ovFvgvEq026wmxXim1jQzu%2FPxckc0fMX0BBf96KKL48%2B7qZ3e3hQeX432M5%2Bb399ogjqJeA3SkcK%2Ffjs7OudOGYTvuP8WbJZZNiQPdGstbbAkQNPpEfeVw1wS6FAHgfVMLPrZms4XtuS0Qs8WIs784g%2B6Sph1UT9PQyxHTlGCLgahuBGI6yJyU%2ByXLzOwDA1MyZUPVrod1t9Asych%2FECb4kvuSrtPsDKphoQ%3D%3D
# &trade_no=2020043022001492160500800408&auth_app_id=2016102300746946&version=1.0&app_id=2016102300746946&sign_type=RSA2&seller_id=2088102180803461&timestamp=2020-04-30+13%3A56%3A53
# 支付检验接口
@api.route('/pay_check', methods=['PUT'])
def pay_check():
    # 转换为字典
    res_dict = request.form.to_dict()
    if not res_dict:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    # 从form接收参数
    sign = res_dict.pop("sign")
    # print(sign)

    # 进行验证

    # 初始化
    alipay = AliPay(
        appid="2016102300746946",
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem"),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/alipay_public_key.pem"),
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True,  # 默认False
    )

    # verify
    success = alipay.verify(res_dict, sign)
    if success:
        # 成功验证
        # 修改订单数据
        order_id = res_dict.get('out_trade_no')
        trade_no = res_dict.get('trade_no')

        try:
            Order.query.filter_by(id=order_id).update({"status": "WAIT_COMMENT", "trade_no": trade_no})
            db.session.commit()
        except Exception as ret:
            db.session.rollback()
            current_app.logger.error(ret)
            return jsonify(errno=RET.DBERR, errmsg='异常，请联系管理员王某某')
        else:
            return jsonify(errno=RET.OK, errmsg='success')

    # 未成功
    else:
        return jsonify(errno=RET.NODATA, errmsg='支付失败')


#  检测支付是否成功
@api.route('/user_pay_check', methods=['GET'])
@login_required
def user_pay_check():
    # 获取信息
    user_id = g.user_id
    # 获取订单id

    # 检验参数
    try:
        orders = Order.query.filter(Order.user_id == user_id,
                                    Order.status == 'WAIT_PAYMENT').all()
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='数据库错误')
        # 若是没有订单
    if not orders:
        return jsonify(errno=RET.OK)

    # 订单存在，进一步处理支付
    orders_id_list = [order.id for order in orders]
    print(len(orders_id_list))

    # 业务处理： 使用python SDK 调用接口
    # 初始化

    alipay = AliPay(
        appid="2016102300746946",
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem"),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/alipay_public_key.pem"),
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True,  # 默认False
    )

    # 调用接口检测
    for order_id in orders_id_list:
        print(order_id)
        response = alipay.api_alipay_trade_query(order_id)

        """
            response = {
              "alipay_trade_query_response": {
                "trade_no": "2017032121001004070200176844",
                "code": "10000",
                "invoice_amount": "20.00",
                "open_id": "20880072506750308812798160715407",
                "fund_bill_list": [
                  {
                    "amount": "20.00",
                    "fund_channel": "ALIPAYACCOUNT"
                  }
                ],
                "buyer_logon_id": "csq***@sandbox.com",
                "send_pay_date": "2017-03-21 13:29:17",
                "receipt_amount": "20.00",
                "out_trade_no": "out_trade_no15",
                "buyer_pay_amount": "20.00",
                "buyer_user_id": "2088102169481075",
                "msg": "Success",
                "point_amount": "0.00",
                "trade_status": "TRADE_SUCCESS",
                "total_amount": "20.00"
              },
              "sign": ""
            }
        """
        # 判断是否成功
        # 取出code
        code = response.get('code')
        # print(type(code))
        # print(type(response.get('trade_status')))
        if code == '10000' and response.get('trade_status') == "TRADE_SUCCESS":
            # 成功
            # 更新状态
            # 成功验证
            # 修改订单数据
            order_id = response.get('out_trade_no')
            trade_no = response.get('trade_no')

            try:
                Order.query.filter_by(id=order_id).update({"status": "WAIT_COMMENT", "trade_no": trade_no})
                db.session.commit()
            except Exception as ret:
                db.session.rollback()
                current_app.logger.error(ret)
                return jsonify(errno=RET.DBERR, errmsg='异常，请联系管理员王某某')

    return jsonify(errno=RET.OK, errmsg='success')
