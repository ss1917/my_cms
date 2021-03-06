#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : shenshuo
date   : 2017年11月15日11:22:08
role   : 权限鉴定类
'''

from settings import settings as app_settings
from models.mg import UserRoles, RoleFunctions, Functions
from libs.db_context import DBContext
import redis


class MyVerify:
    def __init__(self, user_id):
        self.user_id = user_id
        self.method_list = ["GET", "POST", "PATCH", "DELETE", "PUT", "ALL"]
        self.redis_dict = app_settings.get('redises').get('default')
        self.redis_host = self.redis_dict.get('host', '127.0.0.1')
        self.redis_port = self.redis_dict.get('port', 6379)
        self.redis_password = self.redis_dict.get('password', '')
        self.redis_db = self.redis_dict.get('db', '8')
        self.pool = redis.ConnectionPool(host=self.redis_host, port=self.redis_port, password=self.redis_password,
                                         db=self.redis_db, decode_responses=True)

    """
    def write_verify(self):
        rrr = redis.Redis(connection_pool=self.pool)
        for meth in self.methList:
            user_meth = self.user_id + meth
            rrr.delete(user_meth)
        with DBContext('readonly') as session:
            role_list = session.query(UserRoles.role_id).filter(UserRoles.user_id == self.user_id).all()
        for r in role_list:
            func_id_list = session.query(RoleFunctions.func_id).filter(RoleFunctions.role_id == r[0]).all()
            for f in func_id_list:
                func_list = session.query(Functions.method_type, Functions.uri).filter(Functions.func_id == f[0]).all()
                user_meth = self.user_id + func_list[0][0]
                ### 把权限写入redis
                rrr.sadd(user_meth, func_list[0][1])
        return '权限已经写入缓存'
    """

    def write_verify(self):
        rrr = redis.Redis(connection_pool=self.pool)
        for meth in self.method_list:
            user_meth = self.user_id + meth
            rrr.delete(user_meth)
        with DBContext('readonly') as session:
            func_list = session.query(Functions.method_type, Functions.uri
                                      ).outerjoin(RoleFunctions, Functions.func_id == RoleFunctions.func_id).outerjoin(
                UserRoles, RoleFunctions.role_id == UserRoles.role_id).filter(UserRoles.user_id == self.user_id).all()

        for func in func_list:
            ### 把权限写入redis
            rrr.sadd(self.user_id + func[0], func[1])
        return '权限已经写入缓存'

    def get_verify(self, my_method, my_uri):
        rrr = redis.Redis(connection_pool=self.pool)
        all_verify = rrr.smembers(self.user_id + my_method)
        if my_uri in all_verify:
            return 0
        else:
            return -1
