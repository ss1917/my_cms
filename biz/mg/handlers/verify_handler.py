#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : shenshuo
date   : 2017年11月20日15:52:07
role   : 登录、鉴权
'''

from libs.base_handler import BaseHandler
from libs.jwt_token import AuthToken
from libs.my_verify import MyVerify

class SsoHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.write(dict(status=-1, msg='请求类型错误'))

    def post(self, *args, **kwargs):
        auth_key = self.get_argument('auth_key', '')
        authtoken = AuthToken()
        user_info = authtoken.encode_auth_token(auth_key)
        self.write(user_info)


class VerifyHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.write(dict(status='-1', msg='请求类型错误'))

    def post(self, *args, **kwargs):
        auth_key = self.get_argument('auth_key', '')
        meth = self.get_argument('meth', '')
        uri = self.get_argument('uri', '')
        authtoken = AuthToken()
        user_info = authtoken.encode_auth_token(auth_key)
        user_id = user_info.get('user_id','')
        my_verify =MyVerify(user_id)
        if user_id:
            if my_verify.get_verify(meth, uri) == 0:
                self.write(dict(status=0, msg='鉴权成功'))
        else:
            self.write(dict(status=-1, msg='没有权限'))







sso_urls = [
    (r"/v1/accounts/sso/", SsoHandler),
    (r"/v1/accounts/verify/", VerifyHandler),
]

if __name__ == "__main__":
    pass
