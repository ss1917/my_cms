#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : SS
date   : 2017-11-11 12:48:43
role   : 接受任务API
'''

import json
import re
from ast import literal_eval
from libs.mqhelper import MessageQueueBase
from libs.bash_handler import BaseHandler, LivenessProbe
from libs.db_context import DBContext
from models.models import TaskList, TaskSched, TempDetails, TempList


def new_task(list_id, temp_id, *group_list):
    '''根据订单和模板生成任务'''
    with DBContext('default') as session:
        ip_info = session.query(TaskList.hosts).filter(TaskList.list_id == list_id).one()

        for g in group_list:
            temp_info = session.query(TempDetails).filter(TempDetails.temp_id == temp_id, TempDetails.group == g).all()
            for ip in ip_info:
                gip = literal_eval(ip)[g].split(',')
                for i in gip:
                    for t in temp_info:
                        session.add(
                            TaskSched(list_id=list_id, task_group=g, task_level=t.level, task_name=t.cmd_name,
                                      task_cmd=t.command, task_args=t.args, trigger=t.trigger,
                                      exec_user=t.exec_user,
                                      forc_ip=t.forc_ip, exec_ip=i, task_status='1'))

        session.commit()
    return 0


class AcceptTaskHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.write(dict(status=-1,msg='请求方式有误'))

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        print(data)
        ### 首先判断参数是否完整（temp_id，hosts,task_name,submitter）必填
        exec_time = data.get('exec_time', '2038-10-25 14:00:00')
        temp_id = str(data.get('temp_id', None))
        task_name = data.get('task_name', None)
        task_type = data.get('task_type', None)
        submitter = data.get('submitter', None)  ### 应根据登录的用户
        executor = data.get('executor', '')  ### 审批人可以为空
        args = data.get('args', '')  ### 参数，可以为空
        hosts = data.get('hosts', None)  ### 执行主机，不能为空
        details = data.get('details', '')  ### 任务描述
        if not hosts or not temp_id or not task_name or not submitter:
            json_data = {
                'status': -2,
                'msg': '主机,模板ID,提交人不能为空'
            }
            self.write(json_data)

        hosts = literal_eval(hosts)
        group_list = []
        hosts_dic = {}

        with DBContext('readonly') as session:
            all_group = session.query(TempDetails.group).filter(TempDetails.temp_id == temp_id).group_by(
                TempDetails.group).all()

            for g in all_group:
                g = g[0]
                group_list.append(g)
                host = hosts.get(g, None)
                if not host:
                    self.write(dict(status=4, msg="hosts不能为空"))
                    return

                '''
                for ip in host.split(','):
                    if not re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', ip):
                        self.write(dict(status=5, msg="ip格式有误"))
                        return
                '''
                hosts_dic[g] = hosts.get(g, '')

        if set(group_list).issubset(set(hosts.keys())):
            with DBContext('default') as session:
                if not task_type:
                    temp_name = session.query(TempList.temp_name).filter(TempList.temp_id == temp_id).one()
                    task_type = temp_name[0]
                new_list = TaskList(task_name=task_name, task_type=task_type, hosts=str(hosts_dic), args=args,
                                    details=details, descript='', creator=submitter, executor=executor, status='0',
                                    schedule='new', temp_id=temp_id, stime=exec_time)
            session.add(new_list)
            session.commit()
            ### 最后生成任务，若没有接手和执行时间 等待接手和修改最终执行时间
            new_task(new_list.list_id, temp_id, *group_list)
            ### 发送消息
            with MessageQueueBase('task_sced', 'direct', 'the_task') as save_paper_channel:
                save_paper_channel.publish_message(str(new_list.list_id))

            self.write(dict(status=0, msg="任务建立成功,任务ID为：{}".format(new_list.list_id), list_id=new_list.list_id))
        else:
            self.write(dict(status=3, msg="主机分组和模板分组不匹配"))


accept_task_urls = [
    (r"/v1/task/accept/", AcceptTaskHandler),
    (r"/", LivenessProbe)
]
if __name__ == "__main__":
    pass
