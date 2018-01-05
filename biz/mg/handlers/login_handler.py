#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : shenshuo
date   : 2017年11月21日11:51:00
role   : 用户登录
'''

from libs.base_handler import BaseHandler
from libs.jwt_token import AuthToken, gen_md5
from libs.my_verify import MyVerify
import json
import base64
from libs.db_context import DBContext
from models.mg import Users


class LoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        username = data.get('username', None)
        password = data.get('password', None)

        if not username or not password:
            self.write(dict(status=-1, msg='账号密码不能为空'))
            return

        password_md5 = gen_md5(password)
        with DBContext('readonly') as session:
            user_info = session.query(Users).filter(Users.username == username, Users.password == password_md5,
                                                    Users.status != '10').first()

        if not user_info:
            self.write(dict(status=-2, msg='账号密码错误'))
            return

        if user_info.status != '0':
            self.write(dict(status=-3, msg='账号被禁用'))
            return
        user_id = str(user_info.user_id)
        ### 生成token 并写入cookie
        token_info = dict(user_id=user_id, username=user_info.username, nickname=user_info.nickname)
        authtoken = AuthToken()
        auth_key = authtoken.encode_auth_token(**token_info)

        with DBContext('default') as session:
            session.query(Users).filter(Users.username == username).update(
                {Users.last_ip: self.request.headers.get("X-Real-Ip","")})
            session.commit()

        self.set_secure_cookie("username", username)
        self.set_cookie('enable_nickname', base64.b64encode(user_info.nickname.encode('utf-8')))
        self.set_secure_cookie("nickname", user_info.nickname)
        self.set_cookie('auth_key', auth_key, expires_days=1)
        ### 权限写入缓存
        my_verify = MyVerify(user_id)
        my_verify.write_verify()
        self.write(dict(status=0, msg='登录成功'))


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("username")
        self.clear_cookie("user_id")
        self.clear_cookie("auth_key")
        self.redirect("/")

    def post(self):
        self.clear_cookie("username")
        self.clear_cookie("user_id")
        self.clear_cookie("auth_key")
        self.redirect("/")


login_urls = [
    (r"/login/", LoginHandler),
    (r"/logout/", LogoutHandler),
]

if __name__ == "__main__":
    pass
