#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : shenshuo
date   : 2017年11月15日13:43:09
role   : 管理
'''
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from datetime import datetime

Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class OperationRecord(Base):
    __tablename__ = 'operation_record'

    ### 操作记录
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String(50))
    nickname = Column('nickname', String(50))
    method = Column('method', String(10))
    uri = Column('uri', String(150))
    data = Column('data', String(500))
    ctime = Column('ctime', DateTime(), default=datetime.now, onupdate=datetime.now)


class RAServer(Base):
    __tablename__ = 'ra_server'

    ### 记录注册服务器
    service_id = Column('service_id', Integer, primary_key=True, autoincrement=True)
    service = Column('service', String(200))
    ticket = Column('ticket', String(80))
    details = Column('details', String(50))
    ctime = Column('ctime', DateTime(), default=datetime.now, onupdate=datetime.now)


class Users(Base):
    __tablename__ = 'users'

    ### 用户表
    user_id = Column('user_id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String(50), unique=True)
    password = Column('password', String(100))
    nickname = Column('nickname', String(100))
    email = Column('email', String(50))  ### 邮箱
    tel = Column('tel', String(11))  ### 手机号
    wechat = Column('wechat', String(50))  ### 微信号
    no = Column('no', String(50))  ### 工号
    department = Column('department', String(50))  ### 部门
    google_key = Column('google_key', String(80))  ### 谷歌认证秘钥
    superuser = Column('superuser', String(5), default='10')  ### 超级用户  0代表超级用户
    status = Column('status', String(5), default='0')
    last_ip = Column('last_ip', String(18), default='')
    last_login = Column('last_login', DateTime(), default=datetime.now, onupdate=datetime.now)
    ctime = Column('ctime', DateTime(), default=datetime.now)


class Roles(Base):
    __tablename__ = 'roles'

    ### 角色表
    role_id = Column('role_id', Integer, primary_key=True, autoincrement=True)
    role_name = Column('role_name', String(30))
    status = Column('status', String(5), default='0')
    ctime = Column('ctime', DateTime(), default=datetime.now, onupdate=datetime.now)


class UserRoles(Base):
    __tablename__ = 'user_roles'

    ### 用户角色关联表
    user_role_id = Column('user_role_id', Integer, primary_key=True, autoincrement=True)
    role_id = Column('role_id', String(11))
    user_id = Column('user_id', String(11))
    status = Column('status', String(5), default='0')
    utime = Column('utime', DateTime(), default=datetime.now, onupdate=datetime.now)
    ctime = Column('ctime', DateTime(), default=datetime.now)


class Functions(Base):
    __tablename__ = 'functions'

    ### 权限表
    func_id = Column('func_id', Integer, primary_key=True, autoincrement=True)
    func_name = Column('func_name', String(60))
    uri = Column('uri', String(300))
    method_type = Column('method_type', String(10))
    status = Column('status', String(5), default='0')
    utime = Column('utime', DateTime(), default=datetime.now, onupdate=datetime.now)
    ctime = Column('ctime', DateTime(), default=datetime.now)


class RoleFunctions(Base):
    __tablename__ = 'role_functions'

    ### 角色权限关联表
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    role_id = Column('role_id', String(11))
    func_id = Column('func_id', String(11))
    status = Column('status', String(5), default='0')
    utime = Column('utime', DateTime(), default=datetime.now, onupdate=datetime.now)
    ctime = Column('ctime', DateTime(), default=datetime.now)


class Menu(Base):
    __tablename__ = 'menus'

    ### 菜单表
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    pid = Column('pid', Integer)
    title = Column('title', String(30))
    font = Column('font', String(30))
    icon = Column('icon', String(30))
    url = Column('url', String(150))
    spread = Column('spread', Boolean)  ### 是否有下一级
    sort = Column('sort', Integer, default=10)  ### 排序
    ctime = Column('ctime', DateTime(), default=datetime.now, onupdate=datetime.now)


class RoleMenus(Base):
    __tablename__ = 'role_menus'

    ### 角色菜单关联表
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    role_id = Column('role_id', String(11))
    menu_id = Column('menu_id', String(11))
    ctime = Column('ctime', DateTime(), default=datetime.now, onupdate=datetime.now)
