# coding:utf-8

from flask import current_app, jsonify, make_response, request
from . import api
from ihome.utils.captcha.captcha import captcha
from ihome.utils.captcha.response_code import RET
from ihome import redis_store, constants
from ihome.models import User
from ihome.libs.yuntongxun.SendTemplateSMS import CCP
from ihome.tasks.send_sms import send_sms
import random


# GET api/v1.0/image_codes/<image_code>
@api.route('/image_codes/<image_code>')
def get_image_code(image_code):
    """
    获取图片验证码
    :param image_code:
    :return:
    """
    # 逻辑处理

    name, text, image_data = captcha.generate_captcha()
    try:
        redis_store.setex("image_code%s" % image_code, constants.IMAGE_CODE_EXPIRE_TIME, text)
    except Exception as re:
        current_app.logger.error(re)
        return jsonify(errno=RET.DATAERR, errmsg='sorry, an error occured')
    # 返回
    resp = make_response(image_data)
    resp.headers['Content-Type'] = 'image/jpg'
    return resp


# GET api/v1.0/sms_codes/<mobile>?image_code=xxx&user_image_code=xxx

# @api.route("/sms_code/<re(r'1[34578]\d{9}'):mobile>")
# def sms_code(mobile):
#     # 接受参数
#     image_code = request.args.get('image_code')
#     user_image_code = request.args.get('user_image_code')
#
#     # 检验参数
#     if not all([image_code, user_image_code]):
#         return jsonify(errno=RET.PARAMERR, errmag='缺少参数')
#
#     # 逻辑处理
#     # 取出redis的真实值比较
#     really_image_code = redis_store.get('image_code%s' % image_code)
#     if really_image_code is None:
#         return jsonify(errno=RET.DBERR, errmsg='验证码过期')
#
#     else:
#         try:
#             redis_store.delete('image_code%s' % image_code)
#         except Exception as re:
#             current_app.logger.error(re)
#             return jsonify(errno=RET.DBERR, errmsg='验证码清除失败')
#
#     # 比较验证码是否正确
#     if really_image_code.lower() != str(user_image_code).lower():
#         return jsonify(errno=RET.DATAERR, errmsg='验证码错误')
#
#     # 短信验证
#     # 查询电话是否注册过
#     user = User.query.filter_by(mobile=mobile).first()
#     if user is not None:
#         return jsonify(errno=RET.DBERR, errmsg='手机号已经注册')
#
#     # 判断时间是否超过60s
#     try:
#         send_sms_code_time = redis_store.get('send_sms_code%s' % mobile)
#     except Exception as re:
#         current_app.logger.error(re)
#     else:
#         if send_sms_code_time is not None:
#             return jsonify(errno=RET.DBERR, errmsg='操作频繁')
#
#     # 发送短信
#     try:
#         cpp = CCP()
#         code = '%d' % random.randint(0, 999999)  # 验证码
#         cpp.sendTempLATEsMS(mobile, [code, constants.SMS_EXPIRE_TIME / 60], 1)
#     except Exception as re:
#         current_app.logger.error(re)
#         return jsonify(errno=RET.THIRDERR, errmsg='第三方系统错误')
#     else:
#         # 设置redis存储验证码
#         try:
#             redis_store.setex('sms_code%s' % mobile, constants.SMS_EXPIRE_TIME, code)
#             redis_store.setex('send_sms_code%s' % mobile, constants.SEND_SMS_TIME_INTERVAL, 1)
#         except Exception as re:
#             current_app.logger.error(re)
#             return jsonify(errno=RET.SERVERERR, errmsg='数据库写入失败')
#
#     # 返回值
#     return jsonify(errno=RET.OK, errmsg='发送成功')


@api.route("/sms_code/<re(r'1[34578]\d{9}'):mobile>")
def sms_code(mobile):
    # 接受参数
    image_code = request.args.get('image_code')
    user_image_code = request.args.get('user_image_code')

    # 检验参数
    if not all([image_code, user_image_code]):
        return jsonify(errno=RET.PARAMERR, errmag='缺少参数')

    # 逻辑处理
    # 取出redis的真实值比较
    really_image_code = redis_store.get('image_code%s' % image_code)
    if really_image_code is None:
        return jsonify(errno=RET.DBERR, errmsg='验证码过期')

    else:
        try:
            redis_store.delete('image_code%s' % image_code)
        except Exception as re:
            current_app.logger.error(re)
            return jsonify(errno=RET.DBERR, errmsg='验证码清除失败')

    # 比较验证码是否正确
    if really_image_code.lower() != str(user_image_code).lower():
        return jsonify(errno=RET.DATAERR, errmsg='验证码错误')

    # 短信验证
    # 查询电话是否注册过
    user = User.query.filter_by(mobile=mobile).first()
    if user is not None:
        return jsonify(errno=RET.DBERR, errmsg='手机号已经注册')

    # 判断时间是否超过60s
    try:
        send_sms_code_time = redis_store.get('send_sms_code%s' % mobile)
    except Exception as re:
        current_app.logger.error(re)
    else:
        if send_sms_code_time is not None:
            return jsonify(errno=RET.DBERR, errmsg='操作频繁')

    # 发送短信
    try:
        code = '%d' % random.randint(0, 999999)  # 验证码
        send_sms.delay(mobile, [code, constants.SMS_EXPIRE_TIME / 60], 1)
    except Exception as re:
        current_app.logger.error(re)
        return jsonify(errno=RET.THIRDERR, errmsg='第三方系统错误')
    else:
        # 设置redis存储验证码
        try:
            redis_store.setex('sms_code%s' % mobile, constants.SMS_EXPIRE_TIME, code)
            redis_store.setex('send_sms_code%s' % mobile, constants.SEND_SMS_TIME_INTERVAL, 1)
        except Exception as re:
            current_app.logger.error(re)
            return jsonify(errno=RET.SERVERERR, errmsg='数据库写入失败')

    # 返回值
    return jsonify(errno=RET.OK, errmsg='发送成功', data={'sms_code': code})
