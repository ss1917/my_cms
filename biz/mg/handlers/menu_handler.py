#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : shenshuo
date   : 2018年1月30日10:49:27
role   : 菜单管理
'''

from libs.base_handler import BaseHandler
from libs.db_context import DBContext
from models.mg import UserRoles, Menu, RoleMenus, model_to_dict
from libs.auth_login import auth_login_redirect


class MenuHandler(BaseHandler):
    @auth_login_redirect
    def get(self, *args, **kwargs):
        menu_id = self.get_argument('menu_id', default=None, strip=True)
        nav = self.get_argument('nav', default=None, strip=True)
        mlist = []
        rlist = []
        user_id = self.get_current_id()

        if nav == 'list':
            menu_name = 'name'
        else:
            menu_name = 'title'

        with DBContext('readonly') as session:
            my_roles = session.query(RoleMenus.menu_id).outerjoin(UserRoles,
                                                                  RoleMenus.role_id == UserRoles.role_id).filter(
                UserRoles.user_id == user_id).all()
            for r in my_roles:
                rlist.append(int(r[0]))

            all_menu = session.query(Menu).order_by(Menu.sort).all()
            for m in all_menu:
                data_dict = model_to_dict(m)
                if m.id in rlist or self.is_superuser():
                    data_dict.pop('ctime')
                    mlist.append(data_dict)
                elif nav == 'list':
                    data_dict.pop('ctime')
                    mlist.append(data_dict)

        def getchildren(id=0):
            sz = []
            for obj in mlist:
                if obj["pid"] == id:
                    sz.append({"id": obj["id"], "pid": obj["pid"], menu_name: obj["title"], "font": obj["font"],
                               "icon": obj["icon"], "url": obj["url"], "spread": obj["spread"], "sort": obj["sort"],
                               "children": getchildren(obj["id"])})
            return sz

        if menu_id:
            mlist = []
            for m in all_menu:
                data_dict = model_to_dict(m)
                if m.id == int(menu_id):
                    data_dict.pop('ctime')
                    mlist.append(data_dict)
            self.write(dict(code=0, msg='成功', data=mlist))
            return

        self.write(dict(code=0, msg='成功', data=getchildren()))
        return


menu_urls = [
    (r"/v1/accounts/menu/", MenuHandler),
]

if __name__ == "__main__":
    pass
