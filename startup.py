#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : shenshuo
date   : 2017年11月14日20:11:27
role   : 启动程序
'''

import fire
from tornado.options import define
from libs.program import MainProgram
from settings import settings as app_settings
from biz.tasks.program import Application as DealApp
from biz.tasks.applications import Application as AcceptApp
from biz.mg.applications import Application as MgApp
from biz.publish_code.applications import Application as PublishApp

define("service", default='control_api', help="start service flag", type=str)
class MyProgram(MainProgram):
    def __init__(self, service='control_api', progressid=''):
        self.__app = None
        settings = app_settings
        if service == 'mg':
            self.__app = MgApp(**settings)
        if service == 'publish':
            self.__app = PublishApp(**settings)
        if service == 'acceptance':
            self.__app = AcceptApp(**settings)
        elif service == 'exec_task':
            self.__app = DealApp(**settings)
        super(MyProgram, self).__init__(progressid)
        self.__app.start_server()

if __name__ == '__main__':
    fire.Fire(MyProgram)