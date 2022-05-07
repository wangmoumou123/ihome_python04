# coding: utf-8

from celery import Celery
from ihome.libs.yuntongxun.SendTemplateSMS import CCP

app_celery = Celery('ihome', broker='redis://127.0.0.1:6379/1')


@app_celery.task
def send_sms(to, datas, tempId):
    cpp = CCP()
    cpp.sendTempLATEsMS(to, datas, tempId)

