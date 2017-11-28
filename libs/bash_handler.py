#!/usr/bin/env python
# -*-coding:utf-8-*-

from tornado.web import RequestHandler, HTTPError


class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

    def get_current_id(self):
        return self.get_secure_cookie("user_id")

    def write_error(self, status_code, **kwargs):
        if status_code in (404, 403):
            message = None
            if 'exc_info' in kwargs and \
                            kwargs['exc_info'][0] == HTTPError:
                message = kwargs['exc_info'][1].log_message
            self.render('subgroup/404.html', message=message)

        elif status_code == 500:
            self.render('subgroup/404.html', message=None)

        elif status_code == 401:
            self.set_status(status_code)
            self.set_header('WWW-Authenticate', 'Basic realm="cms"')
            self.write("Access denied")
        else:
            self.set_status(status_code)


class LivenessProbe(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("I'm OK")
