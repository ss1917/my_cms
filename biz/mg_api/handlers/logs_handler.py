#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : shenshuo
date   : 2017年11月15日11:22:08
role   : system log
'''

from libs.bash_handler import BaseHandler
from models.mg import OperationRecord, model_to_dict
from libs.db_context import DBContext
from libs.auth_login import auth_login_redirect


class LogHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        page_size = self.get_argument('page', default=1, strip=True)
        limit = self.get_argument('limit', default=10, strip=True)
        username = self.get_argument('username', default=None, strip=True)
        limit_start = (int(page_size) - 1) * int(limit)
        log_list = []
        with DBContext('readonly') as session:
            count = session.query(OperationRecord).count()
            log_info = session.query(OperationRecord).order_by(-OperationRecord.ctime).offset(limit_start).limit(
                int(limit))

            if username:
                log_info = session.query(OperationRecord).filter(
                    OperationRecord.username.like(username + '%')).order_by(-OperationRecord.ctime).offset(
                    limit_start).limit(int(limit))

        for msg in log_info:
            data_dict = model_to_dict(msg)
            data_dict['ctime'] = str(data_dict['ctime'])
            log_list.append(data_dict)

        kwargs = {
            "data": log_list,
            "code": 0,
            "count": count,
            "msg": '获取成功'
        }
        self.write(kwargs)

    @auth_login_redirect
    def post(self, *args, **kwargs):
        method = self.get_argument('method', default='', strip=True)
        uri = self.get_argument('uri', strip=True)
        with DBContext('default') as session:
            session.add(OperationRecord(username='12', method=method, uri=uri))
            session.commit()

        self.write(dict(status=0, msg='写入成功'))


log_urls = [
    (r"/v1/opt_log/", LogHandler),
]

if __name__ == "__main__":
    pass
