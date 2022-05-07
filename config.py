# coding:utf-8

import redis


class Config(object):
    SECRET_KEY = 'DASGFAGffaeaf24r3672%34%r34512'
    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:1234@127.0.0.1:3306/ihome_python04"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # 设置flask—session
    SESSION_TYPE = "redis"  # 设施session存储方式
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 设置redis实例
    SESSION_USE_SIGNER = True  # session加密
    PERMANENT_SESSION_LIFETIME = 86400  # 设置session时间，单位s


# 创建开发
class Development(Config):
    DEBUG = True

    pass


# 创建线上
class Production(Config):
    pass


conf_dict = {'Develop': Development,
             'Product': Production}
