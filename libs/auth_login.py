#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : shenshuo
date   : 2017年11月15日11:22:08
role   : 登录装饰器
'''

import requests
import json
import base64
from settings import settings as app_settings
from libs.jwt_token import AuthToken
from models.mg import Users, OperationRecord
from libs.db_context import DBContext
from libs.my_verify import MyVerify
from tornado.web import HTTPError


### 处理刷新页面的请求
def auth_login_redirect(func):
    def inner(self, *args, **kwargs):

        auth_key = self.get_cookie('auth_key', None)
        if not auth_key:
            # 没登录，就让跳到登陆页面
            raise HTTPError(401, 'auth failed')
        else:
            authtoken = AuthToken()
            user_info = authtoken.decode_auth_token(auth_key)
            user_id = user_info.get('user_id', None)
            username = user_info.get('username', None)
            nickname = user_info.get('nickname', None)

            if not user_id:
                raise HTTPError(401, 'auth failed')
            else:
                user_id = str(user_id)
                self.set_secure_cookie("user_id", user_id)
                self.set_cookie('enable_nickname', base64.b64encode(nickname.encode('utf-8')))
                self.set_secure_cookie("nickname", nickname)
                self.set_secure_cookie("username", username)
                my_verify = MyVerify(user_id)

        ### 防止明文cookie被篡改
        enable_nickname = base64.b64decode(self.get_cookie('enable_nickname')).decode('utf-8')
        if self.get_secure_cookie("nickname").decode('utf-8') != enable_nickname:
            raise HTTPError(403, 'cookie error!')

        ### 如果不是超级管理员,开始鉴权
        if not self.is_superuser():

            # 没权限，就让跳到权限页面 0代表有权限，1代表没权限
            if my_verify.get_verify(self.request.method, self.request.uri) != 0:
                '''如果没有权限，就刷新一次权限'''
                my_verify.write_verify()

            if my_verify.get_verify(self.request.method, self.request.uri) == 0:
                raise HTTPError(403, 'request forbidden!')

        ### 写入日志
        if self.request.method != 'GET':
            try:
                data = json.loads(self.request.body.decode("utf-8"))
            except Exception as e:
                pass

            with DBContext('default') as session:
                session.add(OperationRecord(username=username, nickname=nickname, method=self.request.method,
                                            uri=self.request.uri, data=str(data)))
                session.commit()

        func(self, *args, **kwargs)

    return inner


def auth_login_redirect_bak(func):
    def inner(self, *args, **kwargs):
        ###
        ticket = self.get_argument('ticket', None)
        za_server_url = app_settings.get('za_server_url', '')
        za_sso_validate = app_settings.get('za_sso_validate', '')
        za_sso_login = app_settings.get('za_sso_login', '')
        authtoken = AuthToken()

        if ticket:
            '''如果带返回值就去获取用户信息'''
            validate_args = {'service': za_server_url, 'ticket': ticket}
            v = requests.get(za_sso_validate, params=validate_args)
            user_info = json.loads(v.text)
            username = user_info.get('username', '')
            username = 'ss'
            user_id = str(user_info.get('user_id', '2'))
            self.set_secure_cookie("username", username)
            self.set_secure_cookie("user_id", user_id)

            ### 生成生成token 并且写入cookie
            new_token = authtoken.encode_auth_token(user_id, username)
            self.set_cookie('auth_key', new_token, expires_days=1)

            with DBContext('readonly') as session:
                u = session.query(Users.username).filter(Users.username == username).first()
                '''查询数据库是否用当前用户'''
            if u:
                ''' 如果有 获取当前用户权限，并写入redis缓存起来'''
                my_verify = MyVerify(user_id)
                my_verify.write_verify()
            else:
                '''如果没有则把用户信息导入'''
                '''跳转完善信息页面，并且告知必须加入权限才能访问'''
                pass
                ### 如果没有则把用户信息导入
                ### 跳转完善信息页面，并且告知必须加入权限才能访问
        auth_key = self.get_cookie('auth_key')
        if not auth_key:
            '''没登录，就让跳到登陆页面'''
            sso_login_url = za_sso_login + '?service=' + za_server_url + '&target=' + za_server_url
            self.redirect(sso_login_url)
            return
        else:
            user_info = authtoken.decode_auth_token(auth_key)

        ### 权限鉴定
        my_verify = MyVerify(user_id)
        print(my_verify.get_verify(self.request.method, self.request.uri))
        if my_verify.get_verify(self.request.method, self.request.uri) != 0:
            ### 没权限，就跳转提示没有权限页面权限页面
            print('没有权限')
            # self.redirect('')
            return

        # 执行post方法或get方法
        func(self, *args, **kwargs)

    return inner

