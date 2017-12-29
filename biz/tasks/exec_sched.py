#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : SS
date   : 2017-10-11 12:48:43
role   : exec sched
### 任务状态标记 0:新建,1:等待,2:运行中,3:完成,4:错误,5:手动
### 任务组按顺序触发，任务按预设触发，默认顺序执行

'''
import time
import multiprocessing
from libs.logs import Logger
from biz.tasks.exec_tasks import MyExecute
from sqlalchemy import or_
from models.models import TaskList, TaskSched
from libs.db_context import DBContext
from libs.mqhelper import MessageQueueBase


### 接受MQ消息 根据订单ID和分组 多线程执行任务

class DealMQ(MessageQueueBase):
    def __init__(self):
        super(DealMQ, self).__init__(exchange='task_sced',
                                     exchange_type='direct',
                                     routing_key='the_task',
                                     queue_name='deal_task_sched')

    def my_run(self, flow_id, group_id):
        print('xxx',flow_id, group_id)
        ME = MyExecute(flow_id, group_id)
        ME.exec_thread()

    def exec_list_thread(self, lid, *all_gid):
        ### 标记为任务开始
        with DBContext('default') as session:
            session.query(TaskList.list_id).filter(TaskList.list_id == lid).update({TaskList.schedule: 'start'})
            session.query(TaskSched).filter(TaskSched.list_id == lid, TaskSched.trigger ==
                                            'hand').update({TaskSched.task_status: '5'})
            session.commit()

        threads = []
        #####取所有IP###
        for i in all_gid:
            i = i[0]
            print(i)
            if i:
                threads.append(multiprocessing.Process(target=self.my_run, args=(lid, i,)))
        Logger.info("current has %d threads group execution " % len(threads))

        ###开始多线程
        for start_t in threads:
            try:
                start_t.start()
            except UnboundLocalError:
                print('error')
        ###阻塞线程
        for join_t in threads:
            join_t.join()

    def on_message(self, body):
        time.sleep(2)
        try:
            args = int(body)
        except ValueError:
            Logger.error('[*]body type error, must be int,body:(%s)' % str(body, encoding='utf-8'))
            args = 0
        except UnboundLocalError:
            Logger.error('[*]body type error, must be int,body:(%s)' % str(body, encoding='utf-8'))
            args = 0
        print('flow_id is ', args)
        if type(args) == int:
            flow_id = args
            with DBContext('readonly') as session:
                is_exist = session.query(TaskList.list_id).filter(TaskList.list_id == flow_id,
                                                                  TaskList.schedule == 'ready').first()
            ###查询ID是否存在并且未执行
            if is_exist:
                all_group = session.query(TaskSched.task_group).filter(TaskSched.list_id == flow_id).group_by(
                    TaskSched.task_group).all()

                ### 多进程分组执行任务
                self.exec_list_thread(flow_id, *all_group)
                ### 记录并修改状态
                with DBContext('default') as session:
                    session.query(TaskList.list_id).filter(TaskList.list_id == flow_id).update(
                        {TaskList.schedule: 'OK'})
                    session.commit()
                Logger.info("list{0} end of task".format(flow_id))

            else:
                with DBContext('readonly') as session:
                    exist = session.query(TaskList.list_id).filter(TaskList.list_id == flow_id,
                                                                   or_(TaskList.schedule == 'OK',
                                                                       TaskList.schedule == 'start')).first()
                if exist:
                    Logger.info('task list id {0} is start or OK !!!'.format(body))
                else:
                    Logger.error('task list id {0} is not ready !!!'.format(body))
                    time.sleep(8)
                    raise SystemExit(-2)
        else:
            Logger.error('[*]body type error, must be int,body:(%s)' % str(body, encoding='utf-8'))


if __name__ == "__main__":
    pass
