#!/usr/bin/env python
# -*-coding:utf-8-*-

import json, datetime
from libs.bash_handler import BaseHandler
from libs.db_context import DBContext
from models.models import CmdList, TempList, TempDetails, ArgsList, model_to_dict
from libs.auth_login import auth_login_redirect


class CmdHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        cmd_name = self.get_argument('cmd_name', default=None, strip=True)
        page_size = self.get_argument('page', default=1, strip=True)
        limit = self.get_argument('limit', default=10000, strip=True)
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
            self.write(dict(status=-1, msg='模板ID不能为空'))
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

    @auth_login_redirect
    def put(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        group = data.get('group', None)
        level = data.get('level', None)
        trigger = data.get('trigger', '')
        args = data.get('args', '')
        exec_user = data.get('exec_user', 'root')
        did = str(data.get('id', None))

        if not did or not group or not level:
            self.write(dict(status=-1, msg='不能为空'))
            return

        with DBContext('default') as session:
            session.query(TempDetails).filter(TempDetails.id == did).update(
                {TempDetails.group: group, TempDetails.level: level, TempDetails.trigger: trigger,
                 TempDetails.exec_user: exec_user, TempDetails.args: args})
            session.commit()
        self.write(dict(status=0, msg='修改成功'))

    @auth_login_redirect
    def patch(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        cmd_id = str(data.get('cmd_id', None))
        temp_id = str(data.get('temp_id', None))

        if not cmd_id or not temp_id:
            self.write(dict(status=-1, msg='命令和模板都不能为空'))
            return

        with DBContext('readonly') as session:
            cmd_info = session.query(CmdList).filter(CmdList.cmd_id == cmd_id).first()
            print(cmd_info.cmd_name)

        with DBContext('default') as session:
            session.add(TempDetails(temp_id=temp_id, group='999', level='999', cmd_name=cmd_info.cmd_name,
                                    command=cmd_info.command, args=cmd_info.args, trigger='hand', exec_user='root',
                                    forc_ip=cmd_info.forc_ip, creator=self.get_current_user().decode("utf-8")))
            session.commit()
        self.write(dict(status=0, msg='修改成功'))

    @auth_login_redirect
    def delete(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        did = data.get('id', None)
        if not did:
            self.write(dict(status=-1, msg='不能为空'))
            return

        with DBContext('default') as session:
            session.query(TempDetails).filter(TempDetails.id == did).delete(synchronize_session=False)
            session.commit()
        self.write(dict(status=0, msg='删除成功'))


class ArgsHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        args_name = self.get_argument('args_name', default=None, strip=True)
        page_size = self.get_argument('page', default=1, strip=True)
        limit = self.get_argument('limit', default=20, strip=True)
        limit_start = (int(page_size) - 1) * int(limit)
        args_list = []

        with DBContext('readonly') as session:
            count = session.query(ArgsList).count()
            args_info = session.query(ArgsList).order_by(ArgsList.args_id).offset(limit_start).limit(int(limit))

            if args_name:
                args_info = session.query(ArgsList).filter(ArgsList.args_name.like(args_name + '%')).order_by(
                    ArgsList.args_id).offset(limit_start).limit(int(limit))

        for msg in args_info:
            data_dict = model_to_dict(msg)
            data_dict['utime'] = str(data_dict['utime'])
            args_list.append(data_dict)

        kwargs = {
            "data": args_list,
            "code": 0,
            "count": count,
            "msg": '获取成功'
        }
        self.write(kwargs)

    @auth_login_redirect
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        args_name = data.get('args_name', None)
        args_self = data.get('args_self', None)
        if not args_name or not args_self:
            self.write(dict(status=-1, msg='参数不能为空'))
            return

        with DBContext('readonly') as session:
            args_info = session.query(ArgsList).filter(ArgsList.args_name == args_name).first()
        if args_info:
            self.write(dict(status=-2, msg='名称不能重复'))
            return

        with DBContext('default') as session:
            session.add(
                ArgsList(args_name=args_name, args_self=args_self, creator=self.get_current_user().decode("utf-8")))
            session.commit()
        self.write(dict(status=0, msg='添加成功'))

    def put(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        args_id = data.get('args_id', None)
        args_self = data.get('args_self', None)

        if not args_id or not args_self:
            self.write(dict(status=-1, msg='ID不能为空'))
            return

        with DBContext('default') as session:
            session.query(ArgsList).filter(ArgsList.args_id == args_id).update({ArgsList.args_self: args_self})
            session.commit()
        self.write(dict(status=0, msg='编辑成功'))

    @auth_login_redirect
    def delete(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        args_id = data.get('args_id', None)
        if not args_id:
            self.write(dict(status=-1, msg='ID不能为空'))
            return

        with DBContext('default') as session:
            session.query(ArgsList).filter(ArgsList.args_id.in_(args_id)).delete(synchronize_session=False)
            session.commit()
        self.write(dict(status=0, msg='删除成功'))


temp_urls = [
    (r"/v1/task/cmd/", CmdHandler),
    (r"/v1/task/temp/", TempHandler),
    (r"/v1/task/details/", TempDetailsHandler),
    (r"/v1/task/args/", ArgsHandler),
]

if __name__ == "__main__":
    pass
