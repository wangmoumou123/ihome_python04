# -*- coding: utf-8 -*-
import os

import oss2
# from ihome import constants

# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
# auth = oss2.Auth(constants.yourAccessKeyId, constants.yourAccessKeySecret)
auth = oss2.Auth("LTAI5t6Dj9A2rUVVPeg5WWsS", "QrlWceYJxojh0gbrnaV7WoDUVlElK5")
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', 'home1939')


# 必须以二进制的方式打开文件。

def start_up():
    with open('/home/wang/flask_py2/ihome_python04/ihome/static/images/h3.jpg', 'rb') as fileobj:
        # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
        # fileobj.seek(1000, os.SEEK_SET)
        # Tell方法用于返回当前位置。
        # current = fileobj.tell()

        result = bucket.put_object('h3.jpg', fileobj)
        print result.headers
        print result.resp
        print result.crc
        print result.etag
        print result.status
#
#         # # -*- coding: utf-8 -*-
#         # import oss2
#         #
#         # # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
#         # auth = oss2.Auth('<yourAccessKeyId>', '<yourAccessKeySecret>')
#         # # Endpoint以杭州为例，其它Region请按实际情况填写。
#         # bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', '<yourBucketName>')
#         #
#         # # 必须以二进制的方式打开文件。
#         # with open('<yourLocalFile>', 'rb') as fileobj:
#         #     # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
#         #     fileobj.seek(1000, os.SEEK_SET)
#         #     # Tell方法用于返回当前位置。
#         #     current = fileobj.tell()
#         #     bucket.put_object('<yourObjectName>', fileobj)


def start_down():
    # 下载OSS文件到本地文件。如果指定的本地文件存在会覆盖，不存在则新建。
    #  <yourLocalFile>由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
    #  <yourObjectName>表示下载的OSS文件的完整名称，即包含文件后缀在内的完整路径，例如abc/efg/123.jpg。
    bucket.get_object_to_file('home03.jpg', '/home/wang/flask_py2/ihome_python04/ihome/static/images/h3.jpg')


if __name__ == '__main__':
    start_up()
    # start_down()
