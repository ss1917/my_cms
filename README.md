### 内容管理
### 组件栈
- python3.6
- tornado4.5
- rabbitmq
- mysql5.6
- redis


### python3 startup.py --port=8081  --service=mg
- 功能描述：启动内容管理应用
- 约束：暂无
- 参数：暂无

### python3 startup.py --port=8082  --service=submit_jobs
- 功能描述：提交任务
- 约束：暂无
- 参数：暂无

### python3 startup.py --service=exec_task
- 功能描述：从消息队列里获取任务并执行
- 约束：暂无
- 参数：暂无


### python3 startup.py --port=9001  --service=acceptance
- 功能描述：通过参数生成任务，并发送任务到消息队列
- 约束：详见接口文档
- 参数：详见接口文档