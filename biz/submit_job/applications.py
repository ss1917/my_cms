#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : SS
date   : 2017-10-11 12:48:43
role   : task center
'''
from libs.application import Application as myapplication
from biz.submit_job.handlers.project_handler import project_jobs_urls



class Application(myapplication):
    def __init__(self, **settings):
        urls = []
        urls.extend(project_jobs_urls)
        super(Application, self).__init__(urls, **settings)


if __name__ == '__main__':
    pass