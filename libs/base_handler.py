#!/usr/bin/env python
# -*-coding:utf-8-*-

from tornado.web import RequestHandler, HTTPError
from models.mg import Users
from libs.db_context import DBContext


class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

    def get_current_id(self):
        return self.get_secure_cookie("user_id")

    def get_current_nickname(self):
        return self.get_secure_cookie("nickname")

    def is_superuser(self):
        user_id = self.get_current_id()
        with DBContext('readonly') as session:
            user_info = session.query(Users).filter(Users.user_id == user_id, Users.superuser == '0',
                                                    Users.status == '0').first()
        if user_info:
            return True
        return False

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.set_status(status_code)
            self.write('页面被外星人劫持了')
            return

        elif status_code == 403:
            self.set_status(status_code)
            self.finish('sorry, request forbidden!')

        elif status_code == 500:
            self.set_status(status_code)
            self.finish('服务器内部错误')

        elif status_code == 401:
            self.set_status(status_code)
            self.redirect("/login/")
            return
        else:
            self.set_status(status_code)


class LivenessProbe(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("I'm OK")
