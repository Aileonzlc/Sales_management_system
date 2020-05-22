# gunicorn/django  服务监听地址、端口
bind = '127.0.0.1:8000'

# gunicorn worker 进程个数，建议为： CPU核心个数 * 2 + 1
workers = 3

# gunicorn worker 类型， 使用异步的event类型IO效率比较高
worker_class = "gevent"

# 日志文件路径
errorlog = "/home/aileon/gunicorn.log"
loglevel = "info"

import os
import sys

cwd = os.getcwd()
sys.path.append(cwd)
