#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : ss
date   : 2017年12月22日15:09:46
role   : 处理定时任务
'''

import os
import time
import fire
from datetime import datetime
from models.models import TaskList, TaskSched
from libs.db_context import DBContext


class TaskTimed:
    def exec_task():
        while True:
            time.sleep(5)
            with DBContext('readonly') as session:
                info = session.query(TaskList).filter(TaskList.schedule == 'start',
                                                      TaskList.stime < datetime.now(),
                                                      TaskList.stime > time.localtime(time.time() - 6000)).all()
            for i in info:
                with DBContext('default') as session:
                    session.query(TaskSched).filter(TaskSched.list_id == str(i.list_id), TaskSched.trigger ==
                                                    'timed').update({TaskSched.trigger: 'pass'})
                    session.commit()


def main():
    t = TaskTimed
    t.exec_task()


if __name__ == '__main__':
    fire.Fire(main)
