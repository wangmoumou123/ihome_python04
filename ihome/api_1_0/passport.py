# coding:utf-8
from . import api
from flask import request, jsonify, current_app, session
from ihome.utils.captcha.response_code import RET
from ihome import redis_store, db, constants
from sqlalchemy.exc import IntegrityError
from ihome.models import User
import re


# 注册接口
@api.route("/register", methods=['POST'])
def register():
    # 接收参数,格式为json

    req_dict = request.get_json()
    mobile = req_dict.get('mobile')
    user_sms_code = req_dict.get('user_sms_code')
    password = req_dict.get('password')
    password2 = req_dict.get('password2')

    # 检验参数
    # 检验参数是否玩完整
    if not all([mobile, user_sms_code, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    # 判断手机号是否合法
    if not re.match(r'1[34578]\d{9}', mobile):
        return jsonify(errno=RET.DATAERR, errmsg='参数错误')

    # 判断两次密码是否相等
    if password != password2:
        return jsonify(errno=RET.DATAERR, errmsg='两次密码输入不一致')

    # 判断输入短信验证码是否过期
    try:
        really_sms_code = redis_store.get('sms_code%s' % mobile)
    except Exception as res:
        # 写入日志
        current_app.logger.error(res)
        return jsonify(errno=RET.DBERR, errmsg='验证码不存在')
    else:
        # 判断验证码是否相等
        if user_sms_code != really_sms_code:
            return jsonify(errno=RET.DATAERR, errmsg='短信验证码不正确')

    # 判断手机号是否注册
    # 创建用户
    try:
        user = User(name=mobile, mobile=mobile)
        user.password = password
        db.session.add(user)
        db.session.commit()
    except IntegrityError as res:
        db.session.rollback()
        current_app.logger.error(res)
        return jsonify(errno=RET.DBERR, errmsg='手机号已经注册')
    except Exception as res:
        current_app.logger.error(res)
        return jsonify(errno=RET.DBERR, errmsg='注册失败')

    # 保存登录session
    session['name'] = user.name
    session['mobile'] = mobile
    session['user_id'] = user.id

    # 返回值
    return jsonify(errno=RET.OK, errmsg='注册成功')


# 登录接口
@api.route('/login', methods=['POST'])
def login_page():
    """
    登录函数
    :return: 登陆成功返回 0 , 失败 返回其他对应的值
    """
    # 接收参数
    req_dict = request.get_json()
    mobile = req_dict.get('mobile')
    password = req_dict.get('password')
    # 校验参数
    #  判断参数是否缺少
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    # 判断电话是否合法
    if not re.match(r'1[34578]\d{9}', mobile):
        return jsonify(errno=RET.DATAERR, errmsg='手机号错误')
    # 判断输错次数
    user_ip = request.remote_addr
    try:
        user_wrong_times = redis_store.get('user_ip%s' % user_ip)
    except Exception as ret:
        current_app.logger.error(ret)
    else:
        if user_wrong_times is not None and int(user_wrong_times) >= constants.USER_WRONG_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg='操作频繁，稍后再试')

    # 判断用户名密码是否正确
    try:
        user = User.query.filter_by(mobile=mobile).first()
        # print (user.id)
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='查询信息失败')

    if user is None or not user.check_password(password):
        try:
            # 设置user错误次数
            redis_store.incr('user_ip%s' % user_ip)
            redis_store.expire('user_ip%s' % user_ip, constants.USER_WRONG_LIMIT_TIME)
        except Exception as ret:
            current_app.logger.error(ret)
            return jsonify(errno=RET.DBERR, errmsg='数据库异常')

        return jsonify(errno=RET.DATAERR, errmsg='用户名或密码错误')

    # 保存登录session
    session['name'] = user.name
    session['mobile'] = mobile
    session['user_id'] = user.id
    # 返回
    return jsonify(errno=RET.OK, errmsg='登录成功')


# 主页check_login接口
@api.route('/check_login', methods=['GET'])
def check_login():
    # 接收数据
    name = session.get('name')
    if name is not None:
        return jsonify(errno=RET.OK, errmsg='true', data={'name': name})
    else:
        return jsonify(errno=RET.NODATA, errmsg='false')


# logout接口
@api.route('/logout', methods=['DELETE'])
def logout():
    """
    登出接口
    :return:
    """
    csrf_token = session.get('csrf_token')
    session.clear()
    session['csrf_token'] = csrf_token
    return jsonify(errno=RET.OK, errmsg='true')
