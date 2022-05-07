# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_data, etag
import qiniu.config

import oss2
from ihome import constants

# 需要填写你的 Access Key 和 Secret Key
access_key = 'Q3tQlKQvTcFdwro7N3gDvU7Ib4gHBII6IX07B2FP'
secret_key = 'nf7LKbgAS2ahdFWU4AmhNFFpnlBtMPYt5nD-tt6j'

# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
auth = oss2.Auth(constants.yourAccessKeyId, constants.yourAccessKeySecret)
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', 'home1939')


# 必须以二进制的方式打开文件。

def storage(file_data,name):
    """
    上传文件到七牛
    :param file_data:
    :return:
    """
    # 构建鉴权对象
    # q = Auth(access_key, secret_key)

    # 要上传的空间
    # bucket_name = 'ihome-python9966'

    # # 上传后保存的文件名
    # key = 'my-python-logo.png'

    # 生成上传 Token，可以指定过期时间等
    # token = q.upload_token(bucket_name, None, 3600)

    # # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'

    # with open('/home/wang/flask_py2/ihome_python04/ihome/static/images/h3.jpg', 'rb') as fileobj:
    # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
    # fileobj.seek(1000, os.SEEK_SET)
    # Tell方法用于返回当前位置。
    # current = fileobj.tell()

    result = bucket.put_object(name, file_data)

    # print result.headers
    # print result.resp
    # print result.crc
    # print result.etag
    # print "状态吗:"
    if result.status == 200:
        # print "shuchule "
        return name
    else:
        raise Exception('上传失败')
    #
    # ret, info = put_data(token, None, file_data)
    # print(info)
    # print (ret)
    #

    # if info.status_code == 200:
    #     # 上传成功
    #     return ret.get('key')


if __name__ == '__main__':
    with open('./1.jpg', 'rb')as f:
        file_data = f.read()
    storage(file_data,"ceshi.jpg")
