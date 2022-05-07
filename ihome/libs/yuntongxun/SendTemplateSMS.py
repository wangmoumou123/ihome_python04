# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from CCPRestSDK import REST
import ConfigParser

# ���ʺ�
accountSid = '8aaf0708719c17e00171a228f36a051e'

# ���ʺ�Token
accountToken = '90e41fb1d2a74a87a1feac2a29f63487'

# Ӧ��Id
appId = '8aaf0708719c17e00171a228f3d70525'

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com'

# ����˿�
serverPort = '8883'

# REST�汾��
softVersion = '2013-12-26'


# ����ģ�����
# @param to �ֻ�����
# @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
# @param $tempId ģ��Id

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
            # �ɹ�����0
            return 0
        else:
            # ʧ�ܷ���-1
            return -1
        

if __name__ == '__main__':
    ccp = CCP()
    ccp.sendTempLATEsMS('15225433210', ['980622', '3'], 1)

# def sendTemplateSMS(to, datas, tempId):
#     # ��ʼ��REST yuntongxun
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

# sendTemplateSMS(�ֻ�����,��������,ģ��Id)
