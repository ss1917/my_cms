#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : SS
date   : 2017-10-11 12:48:43
role   : task center
'''
from libs.application import Application as myapplication
from biz.mg.handlers.logs_handler import log_urls
from biz.mg.handlers.verify_handler import sso_urls
from biz.mg.handlers.users_handler import user_mg_urls
from biz.mg.handlers.login_handler import login_urls
from biz.mg.handlers.index_handler import index_urls


class Application(myapplication):
    def __init__(self, **settings):
        urls = []
        urls.extend(log_urls)
        urls.extend(sso_urls)
        urls.extend(user_mg_urls)
        urls.extend(login_urls)
        urls.extend(index_urls)
        super(Application, self).__init__(urls, **settings)


if __name__ == '__main__':
    pass