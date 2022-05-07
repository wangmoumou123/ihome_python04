# coding: utf-8

from . import api
from flask import request, jsonify, current_app, session
from ihome import redis_store, db
from ihome.models import User
from ihome.utils.captcha.response_code import RET
from werkzeug.security import check_password_hash
import re


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

    # 判断用户名密码是否正确
    try:
        user = User.query.filter_by(mobile=mobile).first()
        # print (user.id)
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='用户未注册')

    if user:
        # 取出password_hash
        password_hash = user.password_hash
        # 判断密码是否正确
        instance = check_password_hash(password_hash, password)
        # print (instance)
        if not instance:
            return jsonify(errno=RET.DATAERR, errmsg='密码错误')

        # 保存登录session
        session['name'] = user.name
        session['mobile'] = mobile
        session['user_id'] = user.id

    # 返回
    return jsonify(errno=RET.OK, errmsg='登录成功')

