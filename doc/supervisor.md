```
[group:yunwei_task]
programs=exec_task,acceptance,mg,task_timed

[program:acceptance]
command=python3 startup.py --service=acceptance --port=91%(process_num)02d
process_name=%(program_name)s_%(process_num)02d
numprocs=3
directory=/home/dev/python_dev/my_cms
user=root
autostart = true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/acceptance.log
loglevel=info
logfile_maxbytes=100MB
logfile_backups=3
```

```
[program:mg]
command=python3 startup.py --service=mg --port=90%(process_num)02d
process_name=%(program_name)s_%(process_num)02d
numprocs=3
directory=/home/dev/python_dev/my_cms
user=root
autostart = true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/mg.log
loglevel=info
logfile_maxbytes=100MB
logfile_backups=3
```

```
[program:exec_task]
command=python3 startup.py --service=exec_task
process_name=%(program_name)s_%(process_num)02d
numprocs=20
directory=/home/dev/python_dev/my_cms
user=root
autostart = true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/exec_task.log
loglevel=info
logfile_maxbytes=100MB
```

```
[program:task_timed]
command=python3 task_timed.py
process_name=%(program_name)s_%(process_num)02d
numprocs=1
directory=/home/dev/python_dev/my_cms
user=root
autostart = true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/task_timed.log
loglevel=info
logfile_maxbytes=100MB
```