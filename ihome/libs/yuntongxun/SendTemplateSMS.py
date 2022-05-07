# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from CCPRestSDK import REST
import ConfigParser

# 主帐号
accountSid = '8aaf0708719c17e00171a228f36a051e'

# 主帐号Token
accountToken = '90e41fb1d2a74a87a1feac2a29f63487'

# 应用Id
appId = '8aaf0708719c17e00171a228f3d70525'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

class CCP(object):
    instance = None

    def __new__(cls):
        if not cls.instance:
            obj = super(CCP, cls).__new__(cls)
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls.instance = obj
            return cls.instance

    def sendTempLATEsMS(self, to, datas, tempId):
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        """
        for k, v in result.iteritems():

            if k == 'templateSMS':
                for k, s in v.iteritems():
                    print '%s:%s' % (k, s)
            else:
                print '%s:%s' % (k, v)
        """
        code = result.get('statusCode')
        if code == '00000':
            # 成功返回0
            return 0
        else:
            # 失败返回-1
            return -1
        

if __name__ == '__main__':
    ccp = CCP()
    ccp.sendTempLATEsMS('15225433210', ['980622', '3'], 1)

# def sendTemplateSMS(to, datas, tempId):
#     # 初始化REST yuntongxun
#     rest = REST(serverIP, serverPort, softVersion)
#     rest.setAccount(accountSid, accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to, datas, tempId)
#     for k, v in result.iteritems():
#
#         if k == 'templateSMS':
#             for k, s in v.iteritems():
#                 print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)

# sendTemplateSMS(手机号码,内容数据,模板Id)
