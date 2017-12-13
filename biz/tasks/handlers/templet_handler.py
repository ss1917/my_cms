#!/usr/bin/env python
# -*-coding:utf-8-*-

import json, datetime
from ast import literal_eval
from libs.bash_handler import BaseHandler
from libs.db_context import DBContext
from models.models import CmdList, TempList, TempDetails, ArgsList, model_to_dict
from libs.auth_login import auth_login_redirect


class CmdHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        cmd_name = self.get_argument('cmd_name', default=None, strip=True)
        page_size = self.get_argument('page', default=1, strip=True)
        limit = self.get_argument('limit', default=20, strip=True)
        limit_start = (int(page_size) - 1) * int(limit)
        cmd_list = []

        with DBContext('readonly') as session:
            count = session.query(CmdList).count()
            cmd_info = session.query(CmdList).order_by(CmdList.cmd_id).offset(limit_start).limit(int(limit))

            if cmd_name:
                cmd_info = session.query(CmdList).filter(CmdList.cmd_name.like(cmd_name + '%')).order_by(
                    CmdList.cmd_id).offset(limit_start).limit(int(limit))

        for msg in cmd_info:
            data_dict = model_to_dict(msg)
            data_dict['ctime'] = str(data_dict['ctime'])
            data_dict['utime'] = str(data_dict['utime'])
            cmd_list.append(data_dict)

        kwargs = {
            "data": cmd_list,
            "code": 0,
            "count": count,
            "msg": '获取成功'
        }
        self.write(kwargs)

    @auth_login_redirect
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        cmd_name = data.get('cmd_name', None)
        command = data.get('command', None)
        args = data.get('args', None)
        forc_ip = data.get('forc_ip', None)
        if not cmd_name or not command:
            self.write(dict(status=-1, msg='参数不能为空'))
            return

        with DBContext('readonly') as session:
            cmd_info = session.query(CmdList).filter(CmdList.cmd_name == cmd_name).first()
        if cmd_info:
            self.write(dict(status=-2, msg='名称不能重复'))
            return

        with DBContext('default') as session:
            session.add(CmdList(cmd_name=cmd_name, command=command, args=args, forc_ip=forc_ip,
                                creator=self.get_current_user().decode("utf-8"), ctime=datetime.datetime.now()))
            session.commit()
        self.write(dict(status=0, msg='添加新命令成功'))

    def put(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        cmd_id = data.get('cmd_id', None)
        args = data.get('args', None)
        forc_ip = data.get('forc_ip', None)

        if not cmd_id:
            self.write(dict(status=-1, msg='ID不能为空'))
            return

        with DBContext('default') as session:
            session.query(CmdList).filter(CmdList.cmd_id == cmd_id).update(
                {CmdList.args: args, CmdList.forc_ip: forc_ip})
            session.commit()
        self.write(dict(status=0, msg='编辑成功'))

    @auth_login_redirect
    def delete(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        cmd_id = data.get('cmd_id', None)
        if not cmd_id:
            self.write(dict(status=-1, msg='ID不能为空'))
            return

        with DBContext('default') as session:
            session.query(CmdList).filter(CmdList.cmd_id.in_(cmd_id)).delete(synchronize_session=False)
            session.commit()
        self.write(dict(status=0, msg='删除成功'))


class TempHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        page_size = self.get_argument('page', default=1, strip=True)
        limit = self.get_argument('limit', default=200, strip=True)
        limit_start = (int(page_size) - 1) * int(limit)
        temp_list = []

        with DBContext('readonly') as session:
            count = session.query(TempList).count()
            temp_info = session.query(TempList).order_by(TempList.temp_id).offset(limit_start).limit(int(limit))

        for msg in temp_info:
            data_dict = model_to_dict(msg)
            data_dict.pop('ctime')
            data_dict.pop('utime')
            temp_list.append(data_dict)

        kwargs = {
            "data": temp_list,
            "code": 0,
            "count": count,
            "msg": '获取成功'
        }
        self.write(kwargs)

    @auth_login_redirect
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        temp_name = data.get('temp_name', None)
        if not temp_name:
            self.write(dict(status=-1, msg='模板名称不能为空'))
            return

        with DBContext('readonly') as session:
            info = session.query(TempList).filter(TempList.temp_name == temp_name).first()
        if info:
            self.write(dict(status=-2, msg='模板已存在'))
            return

        with DBContext('default') as session:
            session.add(TempList(temp_name=temp_name, creator=self.get_current_user().decode("utf-8"),
                                 ctime=datetime.datetime.now()))
            session.commit()
        self.write(dict(status=0, msg='创建成功'))

    @auth_login_redirect
    def delete(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        temp_id = data.get('temp_id', None)
        if not temp_id:
            self.write(dict(status=-1, msg='不能为空'))
            return

        with DBContext('default') as session:
            session.query(TempList).filter(TempList.temp_id == temp_id).delete(synchronize_session=False)
            session.commit()
        self.write(dict(status=0, msg='删除成功'))


class TempDetailsHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        temp_id = self.get_argument('temp_id', default=None, strip=True)
        temp_list = []
        if not temp_id:
            self.write(dict(status=-1, msg='ID不能为空'))
            return

        with DBContext('readonly') as session:
            temp_info = session.query(TempDetails).filter(TempDetails.temp_id == temp_id).order_by(TempDetails.group,
                                                                                                   TempDetails.level).all()

        for msg in temp_info:
            data_dict = model_to_dict(msg)
            data_dict.pop('utime')
            temp_list.append(data_dict)

        kwargs = {
            "data": temp_list,
            "code": 0,
            "msg": '获取成功'
        }
        self.write(kwargs)

    def patch(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        group = data.get('group', None)
        level = data.get('level', None)
        trigger = data.get('trigger', None)
        exec_user = data.get('exec_user', None)
        did = str(data.get('id', None))

        if not did:
            self.write(dict(status=-1, msg='不能为空'))
            return

        with DBContext('default') as session:
            session.query(TempDetails).filter(TempDetails.id == did).update(
                {TempDetails.group: group, TempDetails.level: level, TempDetails.trigger: trigger,
                 TempDetails.exec_user: exec_user})
            session.commit()
        self.write(dict(status=0, msg='修改成功'))


temp_urls = [
    (r"/v1/task/cmd/", CmdHandler),
    (r"/v1/task/temp/", TempHandler),
    (r"/v1/task/details/", TempDetailsHandler),
]

if __name__ == "__main__":
    pass
