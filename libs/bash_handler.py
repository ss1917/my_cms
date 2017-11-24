#!/usr/bin/env python
# -*-coding:utf-8-*-

from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

    def get_current_id(self):
        return self.get_secure_cookie("user_id")

class LivenessProbe(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("I'm OK")
