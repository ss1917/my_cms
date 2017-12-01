#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : shenshuo
date   : 2017年11月30日15:55:48
role   : 任务管理API
任务状态标记   0:新建,1:等待,2:运行中,3:完成,4:错误,5:手动
'''

import json
from libs.bash_handler import BaseHandler
from libs.db_context import DBContext
from models.models import TaskList, TaskSched, model_to_dict
from libs.auth_login import auth_login_redirect


class TaskListHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        page_size = self.get_argument('page', default=1, strip=True)
        limit = self.get_argument('limit', default=10, strip=True)
        limit_start = (int(page_size) - 1) * int(limit)
        task_list = []
        with DBContext('readonly') as session:
            count = session.query(TaskList).filter(TaskList.schedule != 'end').count()
            task_info = session.query(TaskList).filter(TaskList.schedule != 'end').order_by(-TaskList.stime).offset(
                limit_start).limit(int(limit))

        for msg in task_info:
            data_dict = model_to_dict(msg)
            data_dict['ctime'] = str(data_dict['ctime'])
            data_dict['stime'] = str(data_dict['stime'])
            task_list.append(data_dict)

        kwargs = {
            "data": task_list,
            "code": 0,
            "count": count,
            "msg": '获取成功'
        }
        self.write(kwargs)


class TaskSchedHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        list_id = self.get_argument('list_id', default=1, strip=True)
        group_list = []
        task_list = []
        with DBContext('readonly') as session:
            all_group = session.query(TaskSched.task_group).filter(TaskSched.list_id == list_id).group_by(
                TaskSched.task_group).all()
            task_info = session.query(TaskList).filter(TaskList.list_id == list_id)

        for msg in task_info:
            data_dict = model_to_dict(msg)
            task_list.append(data_dict)

        for g in all_group:
            group_list.append(g[0])

        kwargs = {
            "group_count": len(group_list),
            "group_list": group_list,
            "code": 0,
            "msg": '获取成功'
        }
        print(kwargs)
        self.write(kwargs)


task_list_urls = [
    (r"/v1/task/list/", TaskListHandler),
    (r"/v1/task/sched/", TaskSchedHandler),
]

if __name__ == "__main__":
    pass
