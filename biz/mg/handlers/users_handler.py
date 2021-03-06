#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : shenshuo
date   : 2017年11月20日11:10:29
role   : 用户管理API

status = '0'    正常
status = '10'   逻辑删除
status = '20'   禁用
'''

import json
import shortuuid
import base64
from libs.base_handler import BaseHandler
from libs.db_context import DBContext
from models.mg import Users, Roles, Functions, RoleFunctions, UserRoles, model_to_dict
from libs.auth_login import auth_login_redirect


class UserHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        page_size = self.get_argument('page', default=1, strip=True)
        limit = self.get_argument('limit', default=10, strip=True)
        username = self.get_argument('username', default=None, strip=True)
        limit_start = (int(page_size) - 1) * int(limit)
        user_list = []
        with DBContext('readonly') as session:
            count = session.query(Users).filter(Users.status != '10').count()
            user_info = session.query(Users).filter(Users.status != '10').order_by(Users.user_id).offset(
                limit_start).limit(int(limit))
            if username:
                user_info = session.query(Users).filter(Users.status != '10',
                                                        Users.username.like(username + '%')).order_by(
                    Users.user_id).offset(limit_start).limit(int(limit))

        for msg in user_info:
            data_dict = model_to_dict(msg)
            data_dict.pop('password')
            data_dict.pop('google_key')
            data_dict['last_login'] = str(data_dict['last_login'])
            data_dict['ctime'] = str(data_dict['ctime'])
            user_list.append(data_dict)

        kwargs = {
            "data": user_list,
            "code": 0,
            "count": count,
            "msg": '获取用户成功'
        }
        self.write(kwargs)

    @auth_login_redirect
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        username = data.get('username', None)
        nickname = data.get('nickname', None)
        department = data.get('department', None)
        tel = data.get('tel', None)
        wechat = data.get('wechat', None)
        no = data.get('no', None)
        email = data.get('email', None)
        if not username or not nickname or not department or not tel or not wechat or not no or not email:
            self.write(dict(status=-1, msg='参数不能为空'))
            return

        with DBContext('readonly') as session:
            user_info1 = session.query(Users).filter(Users.username == username).first()
            user_info2 = session.query(Users).filter(Users.tel == tel).first()
        if user_info1:
            self.write(dict(status=-2, msg='用户名已注册'))
            return

        if user_info2:
            self.write(dict(status=-3, msg='手机号已注册'))
            return

        google_key = base64.b32encode(bytes(shortuuid.uuid() + shortuuid.uuid(), encoding="utf-8")).decode("utf-8")

        with DBContext('default') as session:
            session.add(Users(username=username, password='7d491c440ba46ca20fde0c5be1377aec',
                              nickname=nickname, department=department, tel=tel, wechat=wechat, no=no, email=email,
                              google_key=google_key, superuser='10'))
            session.commit()
        self.write(dict(status=0, msg='新用户密码为：shenshuo'))

    @auth_login_redirect
    def delete(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        user_id = data.get('user_id', None)
        if not user_id:
            self.write(dict(status=-1, msg='不能为空'))
            return

        with DBContext('default') as session:
            session.query(Users).filter(Users.user_id.in_(user_id)).delete(synchronize_session=False)
            session.commit()
        self.write(dict(status=0, msg='删除成功'))

    @auth_login_redirect
    def put(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        department = data.get('department', None)
        tel = data.get('tel', None)
        wechat = data.get('wechat', None)
        no = data.get('no', None)
        email = data.get('email', None)
        user_id = data.get('user_id', None)

        if not department or not tel or not wechat or not no or not email or not user_id:
            self.write(dict(status=-1, msg='不能为空'))
            return

        with DBContext('default') as session:
            session.query(Users).filter(Users.user_id == user_id).update(
                {Users.department: department, Users.tel: tel, Users.wechat: wechat, Users.no: no, Users.email: email})
            session.commit()
        self.write(dict(status=0, msg='编辑成功'))

    @auth_login_redirect
    def patch(self, *args, **kwargs):
        '''禁用、启用'''
        data = json.loads(self.request.body.decode("utf-8"))
        user_id = str(data.get('user_id', None))
        msg = '用户不存在'

        if not user_id:
            self.write(dict(status=-1, msg='不能为空'))
            return

        with DBContext('readonly') as session:
            user_status = session.query(Users.status).filter(Users.user_id == user_id, Users.status != 10).first()
        if not user_status:
            self.write(dict(status=-2, msg=msg))
            return

        if user_status[0] == '0':
            msg = '用户禁用成功'
            new_status = '20'

        elif user_status[0] == '20':
            msg = '用户启用成功'
            new_status = '0'

        with DBContext('default') as session:
            session.query(Users).filter(Users.user_id == user_id, Users.status != 10).update({Users.status: new_status})
            session.commit()
        self.write(dict(status=0, msg=msg))


class RoleHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        page_size = self.get_argument('page', default=1, strip=True)
        limit = self.get_argument('limit', default=10, strip=True)
        role_name = self.get_argument('role_name', default=None, strip=True)
        limit_start = (int(page_size) - 1) * int(limit)
        role_list = []
        with DBContext('readonly') as session:
            count = session.query(Roles).filter(Roles.status != '10').count()
            role_info = session.query(Roles).filter(Roles.status != '10').order_by(Roles.role_id).offset(
                limit_start).limit(int(limit))

            if role_name:
                role_info = session.query(Roles).filter(Roles.status != '10',
                                                        Roles.role_name.like(role_name + '%')).order_by(
                    Roles.role_id).offset(limit_start).limit(int(limit))

        for msg in role_info:
            data_dict = model_to_dict(msg)
            data_dict['ctime'] = str(data_dict['ctime'])
            role_list.append(data_dict)

        kwargs = {
            "data": role_list,
            "code": 0,
            "count": count,
            "msg": '获取角色成功'
        }
        self.write(kwargs)

    @auth_login_redirect
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        role_name = data.get('role_name', None)
        if not role_name:
            self.write(dict(status=-1, msg='角色名不能为空'))
            return

        with DBContext('readonly') as session:
            user_info = session.query(Roles).filter(Roles.role_name == role_name).first()
        if user_info:
            self.write(dict(status=-2, msg='角色已注册'))
            return

        with DBContext('default') as session:
            session.add(Roles(role_name=role_name, status='0'))
            session.commit()
        self.write(dict(status=0, msg='角色创建成功'))

    @auth_login_redirect
    def delete(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        role_id = data.get('role_id', None)
        if not role_id:
            self.write(dict(status=-1, msg='不能为空'))
            return

        with DBContext('default') as session:
            session.query(Roles).filter(Roles.role_id.in_(role_id)).delete(synchronize_session=False)
            session.commit()
        self.write(dict(status=0, msg='删除成功'))

    def put(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        role_name = data.get('role_name', None)
        role_id = data.get('role_id', None)

        if not role_name:
            self.write(dict(status=-1, msg='不能为空'))
            return

        with DBContext('default') as session:
            session.query(Roles).filter(Roles.role_id == role_id).update({Roles.role_name: role_name})
            session.commit()
        self.write(dict(status=0, msg='编辑成功'))

    @auth_login_redirect
    def patch(self, *args, **kwargs):
        '''禁用、启用'''
        data = json.loads(self.request.body.decode("utf-8"))
        role_id = str(data.get('role_id', None))
        msg = '用户不存在'

        if not role_id:
            self.write(dict(status=-1, msg='不能为空'))
            return

        with DBContext('readonly') as session:
            role_status = session.query(Roles.status).filter(Roles.role_id == role_id, Roles.status != 10).first()
        if not role_status:
            self.write(dict(status=-2, msg=msg))
            return

        if role_status[0] == '0':
            msg = '禁用成功'
            new_status = '20'

        elif role_status[0] == '20':
            msg = '启用成功'
            new_status = '0'

        with DBContext('default') as session:
            session.query(Roles).filter(Roles.role_id == role_id, Roles.status != 10).update({Roles.status: new_status})
            session.commit()
        self.write(dict(status=0, msg=msg))


class FuncHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        func_list = []
        with DBContext('readonly') as session:
            func_info = session.query(Functions).filter(Functions.status != '10').order_by(Functions.func_id).all()
        for msg in func_info:
            func_list.append(model_to_dict(msg))

        self.write(dict(status=0, data=func_list))


class RoleUserHandler(BaseHandler):
    @auth_login_redirect
    def get(self, role_id):
        role_list = []
        data_dict = {}
        with DBContext('readonly') as session:
            count = session.query(Roles).filter(Roles.status != '10').count()
            role_info = session.query(Roles, UserRoles.user_id,
                                      Users.username, Users.nickname
                                      ).outerjoin(UserRoles, Roles.role_id == UserRoles.role_id).outerjoin(
                Users, Users.user_id == UserRoles.user_id).order_by(Roles.role_id)
        for i in role_info:
            data_dict = model_to_dict(i[0])
            data_dict['ctime'] = str(data_dict['ctime'])
            data_dict['user_id'] = i[1]
            data_dict['username'] = i[2]
            data_dict['nickname'] = i[3]
            role_list.append(data_dict)

        kargs = {
            "data": role_list,
            "count": 1000,
            "code": 0,
        }
        self.write(kargs)


class RoleFuncHandler(BaseHandler):
    @auth_login_redirect
    def get(self, user_id):
        func_list = []
        kargs = {
            "data": str(func_list),
            "status": 0,
        }
        self.write(kargs)


class UserFuncHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        user_id = 2
        with DBContext('readonly') as session:
            func_list = session.query(Functions.method_type, Functions.uri
                                      ).outerjoin(RoleFunctions, Functions.func_id == RoleFunctions.func_id).outerjoin(
                UserRoles, RoleFunctions.role_id == UserRoles.role_id).filter(UserRoles.user_id == user_id).all()

        for func in func_list:
            print(str(user_id) + func[0], func[1])
            data = {func[1]: func[0]}

        kargs = {
            "data": data,
            "status": 0,
        }
        self.write(kargs)


user_mg_urls = [
    (r"/v1/accounts/user/", UserHandler),
    (r"/v1/accounts/role/", RoleHandler),
    (r"/v1/accounts/role_user/(\d+)/", RoleUserHandler),
    (r"/v1/accounts/role_func/(\d+)/", RoleFuncHandler),
    (r"/v1/accounts/user_func/", UserFuncHandler),
    (r"/v1/accounts/func/", FuncHandler),
]

if __name__ == "__main__":
    pass
