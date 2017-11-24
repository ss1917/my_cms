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


class LogHandler(BaseHandler):
    def get(self, *args, **kwargs):
        log_list = []
        with DBContext('readonly') as session:
            my_record = session.query(OperationRecord).limit(1000)
        for msg in my_record:
            log_list.append(model_to_dict(msg))

        kargs = {
            "data": str(log_list),
            "status": 0,
            "msg": '获取成功'
        }
        self.write(kargs)

    def post(self, *args, **kwargs):
        record = self.get_argument('record', default='', strip=True)
        opt_type = self.get_argument('opt_type')
        print(record, opt_type)
        with DBContext('default') as session:
            session.add(OperationRecord(username='12', user_role='12', opt_type=opt_type, record=record))
            session.commit()
        kargs = {
            "status": 0,
            "msg": '写入成功'
        }
        self.write(kargs)


log_urls = [
    (r"/v1/opt_log/", LogHandler),
]

if __name__ == "__main__":
    pass
