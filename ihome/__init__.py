# coding:utf-8

import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
import redis
from config import conf_dict
from logging.handlers import RotatingFileHandler
from ihome.utils.commons import ReConverter

# 创建数据库
db = SQLAlchemy()

# 创建redis
redis_store = None

# 设置月志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级
# 创建日志记录器,指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
# 创建日志记录的格式日志等级输入日志信息的文件名行数日志信息
formatter = logging.Formatter('%(levelname)s%(filename)s:%(lineno)d%(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象(flask app使用的)添加日记录器
logging.getLogger().addHandler(file_log_handler)


# 创建app
def create_app(conf_name):
    """
    创建app
    :param conf_name: 配置名称
    :return: 返回结果
    """
    app = Flask(__name__)
    conf_name = conf_dict.get(conf_name)
    app.config.from_object(conf_name)

    # 初始化db
    db.init_app(app)

    # 初始化redis
    global redis_store
    redis_store = redis.StrictRedis(host=conf_name.REDIS_HOST, port=conf_name.REDIS_PORT)

    # 创建session
    Session(app)

    # 为flask补充csrf防护
    CSRFProtect(app)

    # 添加自定义转换器
    app.url_map.converters['re'] = ReConverter

    # 注册蓝图
    from ihome import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix="/api/v1.0")

    # 导入静态文件蓝图
    from ihome import web_html
    app.register_blueprint(web_html.html)

    return app
