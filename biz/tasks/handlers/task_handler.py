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
from libs.base_handler import BaseHandler
from libs.db_context import DBContext
from models.models import TaskList, TaskSched, TempDetails, TaskLog, ArgsList, model_to_dict
from libs.auth_login import auth_login_redirect


class TaskListHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        page_size = self.get_argument('page', default=1, strip=True)
        list_history = self.get_argument('history', default=None, strip=True)
        limit = self.get_argument('limit', default=10, strip=True)
        limit_start = (int(page_size) - 1) * int(limit)
        task_list = []
        username = self.get_current_user().decode('utf-8')
        if list_history == 'history':
            with DBContext('readonly') as session:
                count = session.query(TaskList).filter(TaskList.schedule == 'OK').count()
                task_info = session.query(TaskList).filter(TaskList.schedule == 'OK').order_by(-TaskList.stime,
                                                                                               -TaskList.list_id).offset(
                    limit_start).limit(int(limit))
        else:
            with DBContext('readonly') as session:
                count = session.query(TaskList).filter(TaskList.schedule != 'OK').count()
                task_info = session.query(TaskList).filter(TaskList.schedule != 'OK').order_by(-TaskList.stime,
                                                                                               -TaskList.list_id).offset(
                    limit_start).limit(int(limit))

        for msg in task_info:
            data_dict = model_to_dict(msg)
            data_dict['username'] = username
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

    @auth_login_redirect
    def put(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        list_id = data.get('list_id', None)
        list_handle = data.get('list_handle', None)
        start_time = data.get('start_time', None)

        if not list_id or not list_handle:
            self.write(dict(status=-1, msg='参数不能为空'))
            return

        if list_handle == "take_over":
            '''接手任务'''
            with DBContext('default') as session:
                session.query(TaskList).filter(TaskList.list_id == list_id).update(
                    {TaskList.executor: self.get_current_user().decode("utf-8")})
                session.commit()
            self.write(dict(status=0, msg='订单接手成功'))
            return

        elif list_handle == "task_release":
            '''释放任务'''
            with DBContext('default') as session:
                session.query(TaskList).filter(TaskList.list_id == list_id).update({TaskList.executor: ''})
                session.commit()
            self.write(dict(status=0, msg='订单接手成功'))
            return

        elif list_handle == "list_stop":
            with DBContext('default') as session:
                session.query(TaskList).filter(TaskList.list_id == list_id).update({TaskList.schedule: 'OK'})
                session.query(TaskSched).filter(TaskSched.list_id == list_id).update({TaskSched.task_status: '3'})
                session.commit()
            self.write(dict(status=0, msg='订单终止成功'))
            return

        elif list_handle == "list_start" and start_time:
            with DBContext('default') as session:
                session.query(TaskList).filter(TaskList.list_id == list_id).update(
                    {TaskList.schedule: 'ready', TaskList.stime: start_time, TaskList.status: '1'})
                session.query(TaskSched).filter(TaskSched.list_id == list_id, TaskSched.task_status == '0').update(
                    {TaskSched.task_status: '1'})
                session.commit()
                self.write(dict(status=0, msg='任务开始成功'))
                return
        self.write(dict(status=-1, msg='未知错误'))
        return


class TaskCheckHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        list_id = self.get_argument('list_id', default=None, strip=True)
        if not list_id:
            self.write(dict(status=-1, msg='订单ID不能为空'))
            return

        with DBContext('readonly') as session:
            task_info = session.query(TaskList).filter(TaskList.list_id == list_id).all()
            argsinfo = session.query(ArgsList.args_name, ArgsList.args_self).all()

        args_record = []
        new_agrs_dict = {}
        for msg in task_info:
            data_dict = model_to_dict(msg)
            data_dict['ctime'] = str(data_dict['ctime'])
            data_dict['stime'] = str(data_dict['stime'])
            data_dict['username'] = self.get_current_user().decode("utf-8")

        args_dict = literal_eval(data_dict.get('args', None))

        if args_dict:
            for k, v in args_dict.items():
                for i in argsinfo:
                    args_record.append(i[1])
                    if i[1] == k:
                        new_agrs_dict[i[0]] = v
                if k not in args_record:
                    new_agrs_dict[k] = v

        data_dict['new_agrs'] = new_agrs_dict
        data_dict['args_keys'] = list(new_agrs_dict.keys())

        self.write(dict(status=0, msg='获取订单信息成功', data=data_dict))


class TaskSchedHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        list_id = self.get_argument('list_id', default=1, strip=True)
        group = self.get_argument('task_group', default=None, strip=True)
        hosts = self.get_argument('exec_ip', default=None, strip=True)
        group_list = []
        sched_list = []
        hand_list = []
        args_record = []
        new_agrs_dict = {}
        username = self.get_current_user().decode('utf-8')

        if not list_id:
            self.write(dict(status=-1, msg='订单ID不能为空'))
            return

        ### 取出手动干预任务
        with DBContext('readonly') as session:
            task_info = session.query(TaskList).filter(TaskList.list_id == list_id).first()
            hand_task = session.query(TempDetails.cmd_name).filter(TempDetails.temp_id == task_info.temp_id,
                                                                   TempDetails.trigger == 'hand').all()
            ### 取出参数
            argsinfo = session.query(ArgsList.args_name, ArgsList.args_self).all()
            args_dict = literal_eval(task_info.args)

        if args_dict:
            for k, v in args_dict.items():
                for i in argsinfo:
                    args_record.append(i[1])
                    if i[1] == k:
                        new_agrs_dict[i[0]] = v
                if k not in args_record:
                    new_agrs_dict[k] = v

        for h in hand_task:
            hand_list.append(h[0])

        ### 根据权限显示操作按钮
        bt_hidden = 'true'
        if username == task_info.executor or self.is_superuser():
            bt_hidden = 'false'

        ### 根据组和执行主机获取数据
        if group and hosts and list_id:
            with DBContext('readonly') as session:
                sched_info = session.query(TaskSched).filter(TaskSched.list_id == list_id,
                                                             TaskSched.task_group == group,
                                                             TaskSched.exec_ip == hosts).order_by(
                    TaskSched.task_group, TaskSched.task_level).all()
            for msg in sched_info:
                data_dict = model_to_dict(msg)
                data_dict['bt_hidden'] = bt_hidden
                sched_list.append(data_dict)
            self.write(dict(code=0, msg='成功', data=sched_list))
            return

        with DBContext('readonly') as session:
            sched_info = session.query(TaskSched).filter(TaskSched.list_id == list_id).order_by(
                TaskSched.task_group, TaskSched.task_level).all()
            all_group = session.query(TaskSched.task_group).filter(TaskSched.list_id == list_id).group_by(
                TaskSched.task_group).all()

        for msg in sched_info:
            data_dict = model_to_dict(msg)
            data_dict['bt_hidden'] = bt_hidden
            sched_list.append(data_dict)

        task_hosts = literal_eval(task_info.hosts)

        for g in all_group:
            hosts = task_hosts.get(g[0], '10.10.10.10').split(',')
            hosts_status = {}
            for h in hosts:
                with DBContext('readonly') as session:
                    slist = session.query(TaskSched.task_status).filter(TaskSched.list_id == list_id,
                                                                        TaskSched.task_group == g[0],
                                                                        TaskSched.exec_ip == h).order_by(
                        TaskSched.task_group, TaskSched.task_level).all()

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
            "task_time": str(task_info.stime),
            "group_list": group_list,
            "hand_list": hand_list,
            "new_agrs": new_agrs_dict,
            "args_keys": list(new_agrs_dict.keys()),
            "code": 0,
            "msg": '获取成功'
        }
        self.write(kwargs)

    @auth_login_redirect
    def put(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        list_id = data.get('list_id', None)
        sched_id = data.get('sched_id', None)
        task_handle = data.get('task_handle', None)
        hand_task = data.get('hand_task', None)

        if task_handle == "all_hand" and list_id:
            if not hand_task:
                self.write(dict(status=-1, msg='任务名称不正确'))
                return

            ### 审批所有
            with DBContext('default') as session:
                session.query(TaskSched).filter(TaskSched.list_id == list_id, TaskSched.task_name == hand_task).update(
                    {TaskSched.task_status: '1', TaskSched.trigger: 'pass_hand'})
                session.commit()
            self.write(dict(status=0, msg='审核成功'))
            return

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
                session.query(TaskSched).filter(TaskSched.sched_id == sched_id).update(
                    {TaskSched.task_status: '1', TaskSched.trigger: 'pass_hand'})
                session.commit()
            self.write(dict(status=0, msg='手动审核成功'))
            return

        self.write(dict(status=-2, msg='参数有误'))


class TaskLogHandler(BaseHandler):
    @auth_login_redirect
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
    (r"/v1/task/check/", TaskCheckHandler),
    (r"/v1/task/sched/", TaskSchedHandler),
    (r"/v1/task/log/", TaskLogHandler),
]

if __name__ == "__main__":
    pass
