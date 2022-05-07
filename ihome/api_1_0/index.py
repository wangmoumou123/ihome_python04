# coding:utf-8

from . import api
from flask import request

# 主页函数
@api.route('/index', methods=['POST'])
def index():
    # 接受session
    request.cookies.get()
    # 处理
    # 返回