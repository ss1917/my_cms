#!/usr/bin/env python
# -*-coding:utf-8-*-

from libs.application import Application as myapplication
from biz.tasks.handlers.accept_task import accept_task_urls
from biz.tasks.handlers.task_handler import task_list_urls
from biz.tasks.handlers.templet_handler import temp_urls

class Application(myapplication):
    def __init__(self, **settings):
        urls = []

        urls.extend(accept_task_urls)
        urls.extend(task_list_urls)
        urls.extend(temp_urls)
        super(Application, self).__init__(urls, **settings)

if __name__ == '__main__':
    pass