import threading
import logging
import os

# 存放公共全局变量，可以让所有线程、所有模块、所有类，共同编辑同一个变量资源

# ------ 语音参数 -------------------------------------------------------------------------
url = 'https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts'
voice = 'aiqi' # 之前用的思悦，给Tina用的艾琪
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
count_file = file_path('config\\count.yaml')
sentences_file = file_path('config\\sentences.yaml')
targets_file = file_path('config\\targets.yaml')
bombs_file = file_path('config\\bombs.yaml')
log_file = file_path('log\\debug.log')

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
        raise ValueError("Suffix Error: %s" % (string))

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
        raise ValueError("number < 0, number: %s" % (number))

def str2str(string):
    seconds = str2seconds(string)
    return seconds2str(seconds)

# ------ 日志工具 -------------------------------------------------------------------------
def log(level, msg):
    logging.log(level, msg)

# ------ 字典工具 -------------------------------------------------------------------------
def search_index(dict, key):
    cur, next, prev = 0, 0, 0

    if key not in dict.keys():
        log(40, '字典中没有这个键。dict.keys(): %s  key: %s' % (dict.keys(), key))
        return (0, 0, 0)

    max = len(dict.keys())
    if max <= 1: return (0, 0, 0)

    for tmp_key in dict.keys():
        if tmp_key == key: break
        cur += 1

    if (cur == max - 1):
        next = 0
    else:
        next = cur + 1

    if (cur == 0):
        prev = max - 1
    else:
        prev = cur - 1

    return (prev, cur, next)
