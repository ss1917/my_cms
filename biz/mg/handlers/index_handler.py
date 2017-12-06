#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : shenshuo
date   : 2017-10-11 12:48:43
role   : 索引页
'''

import json
from libs.bash_handler import BaseHandler, LivenessProbe
from libs.auth_login import auth_login_redirect
from libs.jwt_token import gen_md5
from models.mg import Users
from libs.db_context import DBContext


class IndexHandler(BaseHandler):
    # @authenticated
    @auth_login_redirect
    def get(self, *args, **kwargs):
        self.render('index.html')


class PanelHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        self.render('html/panel/personal.html')

    @auth_login_redirect
    def patch(self, *args, **kwargs):
        greeting = self.get_argument('greeting', 'Hello')
        self.render('html/panel/password.html')


class PasswordHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        username = self.get_current_user()
        self.render('html/panel/password.html', username=username)

    @auth_login_redirect
    def patch(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        old_password = data.get('old_password', None)
        new_password1 = data.get('new_password1', None)
        new_password2 = data.get('new_password2', None)
        username = self.get_current_user()
        if not old_password or not new_password1 or not new_password2 or not username:
            self.write(dict(status=-1, msg='不能有空值'))
            return

        if new_password1 != new_password2:
            self.write(dict(status=-2, msg='新密码输入不一致'))
            return

        with DBContext('readonly') as session:
            user_info = session.query(Users).filter(Users.username == username).first()

        if user_info.password != gen_md5(old_password):
            self.write(dict(status=-3, msg='密码错误'))
            return

        with DBContext('default') as session:
            session.query(Users).filter(Users.username == username).update({Users.password: gen_md5(new_password1)})
            session.commit()

        self.write(dict(
            status=0,
            msg='修改成功',
        ))


class MenuHandler(BaseHandler):
    pass


index_urls = [
    (r"/home/", IndexHandler),
    (r"/", IndexHandler),
    (r"/panel/", PanelHandler),
    (r"/password/", PasswordHandler),
    (r"/menu/", MenuHandler),
    (r"/are_you_ok/", LivenessProbe)

]

if __name__ == "__main__":
    pass
