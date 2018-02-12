#!/usr/bin/env python
# -*-coding:utf-8-*-

import pyotp
import base64
import os
from opssdk.logs import Log
from opssdk.operate import exec_shell
from opssdk.operate import MyCrypt
from opssdk.operate import now_time
from opssdk.operate import is_ip
from opssdk.operate.mysql import MysqlBase
from opssdk.operate.centralization import SaltApi
from opssdk.operate.check import check_disk, check_sys_version, get_ip_address
from opssdk.get_info import json_to_dict, IniToDict

"""
xz_ops_mail@163.com
D4UuzeFRWcaSCyl
"""

from opssdk.operate.mail import Mail

mailto_list = "191715030@qq.com, shenshuo@shinezone.com, 381759019@qq.com"
sm = Mail()
sm.send_mail(mailto_list, '运维', "标题", "内容", 'plain', '/tmp/cof.ini')
"""
:param to_list:  收件人以半角逗号分隔 必填
:param header:   发件名，必填
:param sub:      标题 必填。
:param content:  发件内容 必填。
:param subtype:  发件格式 默认plain，可选 html格式
:param att:      附件 只支持单附件，选填
:return:         True or False
"""

log_path = '/log/yunwei/{0}.log'.format(os.path.basename(__file__))
log_ins = Log('yunwei', log_path)
log_ins.write_log('info', 'ceshi')


def fei(n):
    pre, cur = 0, 1
    while n >= 0:
        yield pre
        n -= 1
        pre, cur = cur, pre + cur

for i in fei(40):
    print(i)
'''
print(json_to_dict('/tmp/cof.json'))
itd = IniToDict('/tmp/cof.ini','config')
print(itd.get_option())
print(itd.get_option('v1'))

print(check_disk())
print(check_sys_version())
print(get_ip_address('lo'))

log_path = '/log/yunwei/%s.log' % (os.path.basename(__file__))
log_ins = Log('yunwei', log_path)
log_ins.write_log('info', 'ceshi')
print(exec_shell('xxx'))
recode, stdout = exec_shell('du -sh')
print(is_ip('192.168.1.1d'))
mycrypt = MyCrypt()



uu = shortuuid.uuid()+ shortuuid.uuid()
aaa = base64.b32encode(bytes('WRG5HQN3RRVLKCBYPUTGAKWKEZBED7FULYLFMNFUJ2RG',encoding="utf-8")).decode("utf-8")
totp = pyotp.TOTP(aaa)   #基于时间生成动态验证码
print (totp.provisioning_uri("shenshuo@devops.shinezone.net.cn"))
print(totp.now())
'''
