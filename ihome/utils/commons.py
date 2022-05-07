# coding:utf-8

from werkzeug.routing import BaseConverter
from flask import session, jsonify, g
from ihome.utils.captcha.response_code import RET
import functools


# 自定义匹配路由
class ReConverter(BaseConverter):
    def __init__(self, url_map, regex):
        super(ReConverter, self).__init__(url_map)
        self.regex = regex


# 登录状态装饰器

def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 从session取出user_id
        user_id = session.get('user_id')
        if user_id is not None:
            g.user_id = user_id
            return func(*args, **kwargs)
        else:
            return jsonify(errno=RET.LOGINERR, errmsg='用户未登陆')

    return wrapper


@login_required
def fun():
    pass
