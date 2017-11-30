#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : SS
date   : 2017-10-11 12:48:43
role   : task center
'''
from libs.application import Application as myapplication
from biz.mg.handlers.logs_handler import log_urls



class Application(myapplication):
    def __init__(self, **settings):
        urls = []
        urls.extend(log_urls)
        super(Application, self).__init__(urls, **settings)


if __name__ == '__main__':
    pass