#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : shenshuo
date   : 2017年12月27日13:37:31
role   : 提交任务
'''

import json
from settings import settings
from libs.fetch_coroutine import fetch_coroutine
from libs.bash_handler import BaseHandler
from libs.auth_login import auth_login_redirect
from tornado.gen import Task, coroutine
from tornado.web import asynchronous


class VersionUpdateHandler(BaseHandler):
    @auth_login_redirect
    @asynchronous
    @coroutine
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        zones = data.get('zones', None)
        version = data.get('version', None)
        sql = data.get('sql', None)
        stop = data.get('stop', None)
        details = data.get('details', None)
        exec_time = data.get('stime', None)
        if not zones:
            self.write(dict(status=-1, msg='区不能为空'))
            return
        if not version and not sql:
            self.write(dict(status=-1, msg='至少需要版本或者数据库更新'))
            return
        zones = ','.join(zones)
        zones = ','.join(set(zones.split(',')))
        args = dict(VERSION=version, SQL=sql, STOP=stop)
        hosts = {1: zones}
        the_body = json.dumps(
            {"task_name": "测试一下", "temp_id": "4", "args": str(args), "details": str(details), "hosts": str(hosts),
             "submitter": self.get_current_user().decode("utf-8"), "exec_time": exec_time})
        ### 协程请求生成任务的API，防止调用阻塞
        url = settings['accept_task_url']
        req = yield Task(fetch_coroutine, url, method='POST', body=the_body)
        return self.write(req)


project_jobs_urls = [
    (r"/v1/jobs/update/", VersionUpdateHandler),
]

if __name__ == "__main__":
    pass
