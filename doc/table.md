```
### 创建数据库
CREATE DATABASE `shenshuo` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

status = '0'   正常
status = '10'   逻辑删除
status = '20'   禁用

##### 操作日志
CREATE TABLE `operation_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `nickname` varchar(50),
  `method` varchar(10) NOT NULL,
  `uri` varchar(150) NOT NULL,
  `data` varchar(200) NOT NULL,
  `ctime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

##### 用户表
CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(100),
  `nickname` varchar(50),
  `email` varchar(50),
  `tel` varchar(11),
  `wechat` varchar(50),
  `no` varchar(50) NOT NULL,
  `department` varchar(50) NOT NULL,
  `superuser` varchar(5) NOT NULL,
  `status` varchar(5) NOT NULL,
  `last_ip` varchar(18) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `ctime` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
insert into users value(2,'ss','xxx','沈硕','111@qq.com','15618718060','kf','10086','开发部','222','0','','','');

##### 角色表
CREATE TABLE `roles` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(30) NOT NULL,
  `status` varchar(5) NOT NULL,
  `ctime` datetime DEFAULT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
insert into roles value(2,'test','0','');

### 用户角色关联表
CREATE TABLE `user_roles` (
  `user_role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` varchar(11) NOT NULL,
  `user_id` varchar(11) NOT NULL,
  `status` varchar(5) NOT NULL,
  `utime` datetime DEFAULT NULL,
  `ctime` datetime DEFAULT NULL,
  PRIMARY KEY (`user_role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
insert into user_roles value(2,'2','2','0','','');

### 权限表
CREATE TABLE `functions` (
  `func_id` int(11) NOT NULL AUTO_INCREMENT,
  `func_name` varchar(60) NOT NULL,
  `uri` varchar(300) NOT NULL,
  `method_type` varchar(10) NOT NULL,
  `status` varchar(5) NOT NULL,
  `utime` datetime DEFAULT NULL,
  `ctime` datetime DEFAULT NULL,
  PRIMARY KEY (`func_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
insert into functions value(2,'test','/test/','GET','0','','');

### 角色权限关联表
CREATE TABLE `role_functions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` varchar(11) NOT NULL,
  `func_id` varchar(11) NOT NULL,
  `status` varchar(5) NOT NULL,
  `utime` datetime DEFAULT NULL,
  `ctime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
insert into role_functions value(2,'2','2','0','','');

##### 任务列表

  CREATE TABLE `task_list` (
  `list_id` int(11) NOT NULL AUTO_INCREMENT,
  `task_name` varchar(50) NOT NULL,
  `task_type` varchar(50) NOT NULL,
  `hosts` longtext NOT NULL,
  `args` longtext NOT NULL,
  `details` longtext NOT NULL,
  `descript` longtext NOT NULL,
  `creator` varchar(50) NOT NULL,
  `executor` varchar(50) NOT NULL,
  `status` varchar(5) NOT NULL,
  `schedule` varchar(50) NOT NULL,
  `temp_id` varchar(12) NOT NULL,
  `ctime` datetime DEFAULT NULL,
  `stime` datetime DEFAULT NULL,
  PRIMARY KEY (`list_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

##### 任务日志表

CREATE TABLE `task_log` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `list_id` varchar(11) NOT NULL,
  `task_group` varchar(5) NOT NULL,
  `task_level` varchar(5) NOT NULL,
  `exec_ip` char(15) NOT NULL,
  `task_log` varchar(250) NOT NULL,
  `log_time` datetime DEFAULT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

##### 任务调度表

CREATE TABLE `task_sched` (
  `sched_id` int(11) NOT NULL AUTO_INCREMENT,
  `list_id` varchar(11) NOT NULL,
  `task_group` varchar(5) NOT NULL,
  `task_level` varchar(5) NOT NULL,
  `task_name` varchar(25) NOT NULL,
  `task_cmd` varchar(128) NOT NULL,
  `task_args` varchar(128) NOT NULL,
  `trigger` varchar(10) NOT NULL,
  `exec_user` varchar(20) NOT NULL,
  `forc_ip` char(15) NOT NULL,
  `exec_ip` char(15) NOT NULL,
  `task_status` varchar(5) NOT NULL,
  PRIMARY KEY (`sched_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

##### 命令表

 CREATE TABLE `cmd_list` (
  `cmd_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmd_name` varchar(25) NOT NULL,
  `command` varchar(250) NOT NULL,
  `args` varchar(250) NOT NULL,
  `forc_ip` char(15) NOT NULL,
  `creator` varchar(30) NOT NULL,
  `ctime` datetime DEFAULT NULL,
  `utime` datetime DEFAULT NULL,
  PRIMARY KEY (`cmd_id`)
) DEFAULT CHARSET=utf8;


##### 模板列表

 CREATE TABLE `temp_list` (
  `temp_id` int(11) NOT NULL AUTO_INCREMENT,
  `temp_name` varchar(25) NOT NULL,
  `creator` varchar(30) NOT NULL,
  `ctime` datetime DEFAULT NULL,
  `utime` datetime DEFAULT NULL,
  PRIMARY KEY (`temp_id`)
) DEFAULT CHARSET=utf8;


#####  模板详情

 CREATE TABLE `temp_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `temp_id` varchar(11) NOT NULL,
  `group` varchar(30) NOT NULL,
  `level` varchar(30) NOT NULL,
  `cmd_name` varchar(30) NOT NULL,
  `command` varchar(128) NOT NULL,
  `args` varchar(128) NOT NULL,
  `trigger` varchar(10) NOT NULL,
  `exec_user` varchar(20) NOT NULL,
  `exec_ip` char(15) NOT NULL,
  `forc_ip` char(15) NOT NULL,
  `creator` varchar(30) NOT NULL,
  `utime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8;

##### 模板列表

 CREATE TABLE `args_list` (
  `args_id` int(11) NOT NULL AUTO_INCREMENT,
  `args_name` varchar(30) NOT NULL,
  `args_self` varchar(50) NOT NULL,
  `creator` varchar(35) NOT NULL,
  `utime` datetime DEFAULT NULL,
  PRIMARY KEY (`args_id`)
) DEFAULT CHARSET=utf8;
```
####测试数据
```
insert into temp_list values(1,'ceshi1','ss','',''),(2,'ceshi2','ss','','');
insert into temp_details value(4,'2','1','2','测试2','echo hello && sleep 10 && ls /tmp','','','root','127.0.0.1','','',''),(5,'2','1','3','测试3','echo arg01 && sleep 10 && ls /tmp','','','root','127.0.0.1','','','');
insert into args_list values(1,'版本','VERSION','ss',''),(2,'环境','ENVI','ss','');
insert into cmd_list value(2,'测试一下2','echo this is a test2','','','','',''),(3,'测试一下3','echo this is a test3','','','','','');
```