#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : shenshuo
date   : 2017年11月15日13:43:09
role   : 管理
'''
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from datetime import datetime

Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class PublishList(Base):
    __tablename__ = 'publish_list'

    ### 发布详情表
    ### 项目新建、已有应用，项目关联整个流程
    publish_id = Column('publish_id', Integer, primary_key=True, autoincrement=True)
    project_name = Column('project_name', String(150))   ### 项目名称
    product_name = Column('product_name', String(100))  ### 产品名称
    department = Column('department', String(200))      ### 部门
    creator = Column('creator', String(50))  ### 负责人
    partake = Column('partake', String(300))  ### 参与人，可以多个
    reviewer = Column('reviewer', String(50))  ### 评审人
    kwargs = Column('kwargs', Text())    ### 其他关键参数,哈希格式
    description = Column('description', Text())  ### 描述
    schedule = Column('schedule', String(10))  ### 进度
    status = Column('status', String(10))  ### 发布状态
    temp_id = Column('temp_id', String(11))  ### 执行模板
    ctime = Column('ctime', DateTime(), default=datetime.now, onupdate=datetime.now)  ### 创建时间
    plan_time = Column('plan_time', DateTime())  ### 计划发布时间

