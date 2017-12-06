#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : shenshuo
date   : 2017年11月30日15:55:48
role   : 任务管理API
任务状态标记   0:新建,1:等待,2:运行中,3:完成,4:错误,5:手动
'''

import json
from ast import literal_eval
from libs.bash_handler import BaseHandler
from libs.db_context import DBContext
from models.models import TaskList, TaskSched, TempDetails, TaskLog, model_to_dict
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
            task_info = session.query(TaskList).filter(TaskList.schedule != 'end').order_by(-TaskList.stime,
                                                                                            -TaskList.list_id).offset(
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
        group = self.get_argument('task_group', default=None, strip=True)
        hosts = self.get_argument('exec_ip', default=None, strip=True)
        group_list = []
        sched_list = []
        if group and hosts and list_id:
            with DBContext('readonly') as session:
                sched_info = session.query(TaskSched).filter(TaskSched.list_id == list_id,
                                                             TaskSched.task_group == group,
                                                             TaskSched.exec_ip == hosts)
            for msg in sched_info:
                data_dict = model_to_dict(msg)
                sched_list.append(data_dict)
            self.write(dict(code=0, msg='成功', data=sched_list))
            return

        with DBContext('readonly') as session:
            sched_info = session.query(TaskSched).filter(TaskSched.list_id == list_id)
            task_info = session.query(TaskList).filter(TaskList.list_id == list_id).first()
            all_group = session.query(TaskSched.task_group).filter(TaskSched.list_id == list_id).group_by(
                TaskSched.task_group).all()

        for msg in sched_info:
            data_dict = model_to_dict(msg)
            sched_list.append(data_dict)

        task_hosts = literal_eval(task_info.hosts)
        task_time = str(task_info.stime)

        for g in all_group:
            hosts = task_hosts.get(str(g[0]), '127.0.0.1').split(',')
            hosts_status = {}
            for h in hosts:
                with DBContext('readonly') as session:
                    slist = session.query(TaskSched.task_status).filter(TaskSched.list_id == list_id,
                                                                        TaskSched.task_group == g[0],
                                                                        TaskSched.exec_ip == h).all()

                status_list = []
                for s in slist:
                    status_list.append(s[0])
                if '0' in status_list:
                    status = '0'
                if '1' in status_list:
                    status = '1'
                if '2' in status_list:
                    status = '2'
                if '5' in status_list and '1' not in status_list and '2' not in status_list:
                    status = '5'
                if '4' in status_list:
                    status = '4'
                if '3' in status_list and len(list(set(status_list))) == 1:
                    status = '3'

                hosts_status[str(h)] = status
            group_list.append(dict(group=g[0], hosts=hosts, task_status=hosts_status))

        kwargs = {
            "data": sched_list,
            "task_time": task_time,
            "group_list": group_list,
            "code": 0,
            "msg": '获取成功'
        }
        self.write(kwargs)

    def put(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        list_id = data.get('list_id', None)
        sched_id = data.get('sched_id', None)
        task_handle = data.get('task_handle', None)
        if not list_id or not sched_id:
            self.write(dict(status=-1, msg='参数不能为空'))
            return

        with DBContext('readonly') as session:
            sched_info = session.query(TaskSched).filter(TaskSched.sched_id == sched_id)

        for msg in sched_info:
            data_dict = model_to_dict(msg)

        if task_handle == "redo":
            ### 重做,把任务修改为等待运行
            with DBContext('default') as session:
                session.query(TaskSched).filter(TaskSched.list_id == list_id,
                                                TaskSched.exec_ip == data_dict['exec_ip'],
                                                TaskSched.task_group == data_dict['task_group'],
                                                TaskSched.task_level >= data_dict['task_level'],
                                                TaskSched.task_status != '5').update({TaskSched.task_status: '1'})
                session.commit()
            self.write(dict(status=0, msg='成功'))
            return

        elif task_handle == "stop":
            ### 终止当前,把当前主机任务组修改为已完成
            with DBContext('default') as session:
                session.query(TaskSched).filter(TaskSched.list_id == list_id,
                                                TaskSched.exec_ip == data_dict['exec_ip'],
                                                TaskSched.task_group == data_dict['task_group']).update(
                    {TaskSched.task_status: '3'})
                session.commit()
            self.write(dict(status=0, msg='终止当前组成功'))
            return

        elif task_handle == "hand":
            ### 手动审批
            with DBContext('default') as session:
                session.query(TaskSched).filter(TaskSched.sched_id == sched_id).update({TaskSched.task_status: '1'})
                session.commit()
            self.write(dict(status=0, msg='手动审核成功'))
            return

        self.write(dict(status=-2, msg='参数有误'))


class TaskLogHandler(BaseHandler):
    def get(self, *args, **kwargs):
        list_id = self.get_argument('list_id', default=1, strip=True)
        group = self.get_argument('task_group', default=None, strip=True)
        level = self.get_argument('task_level', default=None, strip=True)
        hosts = self.get_argument('exec_ip', default=None, strip=True)
        if not list_id or not group or not level or not hosts:
            self.write(dict(status=-1, msg='参数不能为空'))
            return

        log_list = []
        with DBContext('readonly') as session:
            log_info = session.query(TaskLog.log_time, TaskLog.task_log).filter(TaskLog.list_id == list_id,
                                                                                TaskLog.exec_ip == hosts,
                                                                                TaskLog.task_group == group,
                                                                                TaskLog.task_level == level).all()
        for i in log_info:
            data_dict = {}
            data_dict['log_time'] = str(i[0])
            data_dict['task_log'] = str(i[1])
            log_list.append(data_dict)

        self.write(dict(code=0, msg='获取日志成功', data=log_list))


task_list_urls = [
    (r"/v1/task/list/", TaskListHandler),
    (r"/v1/task/sched/", TaskSchedHandler),
    (r"/v1/task/log/", TaskLogHandler),
]

if __name__ == "__main__":
    pass
