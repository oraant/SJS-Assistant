import threading
import logging
import os

# 存放公共全局变量，可以让所有线程、所有模块、所有类，共同编辑同一个变量资源

# ------ 语音参数 -------------------------------------------------------------------------
url = 'https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts'
voice = 'siyue'
appkey = 'isoImgAr3zR2V4Lq'
format = 'mp3'

# ------ 倒计时用 -------------------------------------------------------------------------
seconds = 0
seconds_sem = threading.BoundedSemaphore(1)

# ------ 常用路径 -------------------------------------------------------------------------
# note: os.path.join这个方法简直有病，要join的内容，开头结尾都不要加斜杠！否则无效！

project_name = "SJS-Assistant"
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = cur_path[:cur_path.find(project_name)+len(project_name)]

def file_path(x): return os.path.join(root_path, x)
bombs_file = file_path('config\\bombs.yaml')
words_file = file_path('config\\words.yaml')
targets_file = file_path('config\\targets.yaml')
sentences_file = file_path('config\\sentences.yaml')
logs_file = file_path('log\\debug.log')

# ------ 时间工具 -------------------------------------------------------------------------

# 将20m转换为1200秒
def str2seconds(string):
    if string.isdigit(): string += "m"
    num = int(string[:-1])
    suffix = string[-1]

    if suffix == "h":
        num *= 3600
    elif suffix == "m" or "":
        num *= 60
    elif suffix == "s":
        num = num
    else:
        raise ValueError

    if num < 0:
        num = 0

    return num

# 将1200秒转换为20分钟
def seconds2str(number):
    if number >= 3600:
        return "%.1f" % (number/3600) + "小时"
    elif number >= 60:
        return "%.1f" % (number/60) + "分钟"
    elif number >= 0:
        return "%.1f" % (number) + "秒"
    else:
        raise ValueError

def str2str(string):
    seconds = str2seconds(string)
    return seconds2str(seconds)

# ------ 日志工具 -------------------------------------------------------------------------
def log(level, msg):
    logging.log(level, msg)
