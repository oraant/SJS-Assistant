# === 测试功能 ===============================================

import winsound
from win32com.client import Dispatch
win_speak = Dispatch('SAPI.SPVOICE').Speak  # Windows朗读设备，只能阻塞朗读
win_speak('') # 最好先调用一下，不然在线程里调用的时候，容易出现问题
win_wshshl= Dispatch("WScript.Shell") # 用来发送按键，可以发送组合键

def press_key(systray): win_wshshl.SendKeys('{F13}')
def say_nihao(systray): win_speak('你好')
def make_beep(systray): winsound.Beep(1000, 1000)



# === 读写配置 ===============================================

from ruamel.yaml import YAML; yaml = YAML()
from bin.common import count_file

def get_count(): # 直接从配置文件中读取count值
    with open(count_file, encoding='utf-8') as f:
        return yaml.load(f)['count']

def set_count(count): # 直接像配置文件中读取count值
    with open(count_file, 'w', encoding='utf-8') as f:
        yaml.dump({'count': count}, f)



# === 监控文件 ===============================================

import threading, time, random
from win32gui import GetCursorPos

mc_sleep_gap = 10 # 轮询的间隔
coefficient = 1 # 惩罚的价格，写1就是错1次罚1下，写5就是错1次罚5下

def monitor_config():
    last_position = GetCursorPos()
    while True:
        time.sleep(mc_sleep_gap)
        count = get_count()
        position = GetCursorPos()

        if count <= 0: continue # 设定触发的必要条件：必须有数值才行
        if random.random() > (mc_sleep_gap * coefficient)/3600: continue # 设定触发的概率和强度，系数为1时大概1小时吓1次
        if position == last_position: continue

        press_key(0) # 执行惩罚
        last_position = position
        set_count(count-1)



# === 提醒功能 ===============================================

from datetime import datetime as dt, time as t, timedelta as td
reminder_list = ['23:00', '23:59']
END_OF_TIME = dt(9999, 1, 1)
reminder_temp = END_OF_TIME

def get_reminder(): # 获取下一个该报时的时间点
    next_reminder = ''

    for reminder_t in reminder_list: # 从定时列表中，寻找下一个该报时的时间点（也可能都报过了）
        reminder_dt = dt.combine(dt.now().date(), t.fromisoformat(reminder_t)) # 将单纯的时间与当天的日期绑定
        if dt.now() > reminder_dt: continue # 已经走过的报时就不用管了
        else: next_reminder = reminder_dt; break; # 发现的第一个未报的先记下来

    if (not next_reminder) or (next_reminder > reminder_temp): # 若没有定时报点，或有较早的灵活报点，就修正一下
        next_reminder = reminder_temp

    return next_reminder

def get_delta_str(timedelta): # 将时间差转化为更加流畅的朗读文本（暂不支持隔天）
    h, m, s = str(timedelta).split('.')[0].split(':')
    delta_str = ''

    if int(h) != 0: delta_str += h.lstrip('0') + '小时'
    if int(m) != 0: delta_str += m.lstrip('0') + '分钟'
    if int(s) != 0: delta_str += s.lstrip('0') + '秒'

    return delta_str


mt_sleep_gap = 1 # 监控间隔
alert_list = [1800, 600, 300, 120, 60, 20, 1] # 还有多少秒时要提醒时

def monitor_time():
    global reminder_temp
    while True:
        time.sleep(mt_sleep_gap)
        next_reminder = get_reminder()
        timedelta = next_reminder - dt.now()

        if timedelta.days > 0: continue # 应该是没有设置临时报时的情况，直接跳过既可
        print('next_reminder: ', next_reminder, 'timedelta: ', timedelta)

        for alert_second in alert_list: # 在该报警的时间点报警
            if alert_second - 1 < timedelta.seconds < alert_second + mt_sleep_gap: # 计时制可能不精确，导致错过某一秒，故必须选取一段时间，保证此时间段内报警，且只报警一次（朗读所花费的时间，肯定超过1秒了）
                if alert_second == 600:
                    win_speak('请注意，时间只剩下10分钟了，请5分钟后及时退出。最起码也要做好随时退出的准备。')
                if alert_second == 300:
                    win_speak('请注意，时间只剩下5分钟了，请及时退出。最起码也要做好随时退出的准备。')
                elif alert_second == 1:
                    win_speak('注意！时间到了！请立即矫正自己的行为，否则就要接受音波灌耳的惩罚！警告！警告！十！九！八！七！六！五！四！三！二！一！零！')
                    reminder_temp = END_OF_TIME
                else:
                    win_speak('离%s差%s' % (next_reminder.strftime('%H:%M'), get_delta_str(timedelta)))



# === 注册热键 ===============================================

import keyboard

# 增加惩罚次数
def add_count(num):
    set_count(get_count()+num)
    winsound.Beep(1000, 300)
def add_1(): add_count(1*coefficient)
def add_5(): add_count(5*coefficient)
def add_x(): add_count(10*coefficient)

keyboard.add_hotkey('ctrl+shift+alt+1', add_1)
keyboard.add_hotkey('ctrl+shift+alt+2', add_5)
keyboard.add_hotkey('ctrl+shift+alt+3', add_x)
keyboard.add_hotkey('f21', add_1)
keyboard.add_hotkey('f22', add_5)
keyboard.add_hotkey('f23', add_x)


# 调整计时器

def report_next():
    next_reminder = get_reminder()
    if next_reminder == END_OF_TIME: win_speak('无闹钟')
    else: win_speak('闹钟在：' + get_reminder().strftime('%H:%M'))

def modify_temp():
    global reminder_temp
    if reminder_temp == END_OF_TIME: # 若没设置临时闹钟，则设定为当前时间的五分钟后
        reminder_temp = dt.now() + td(minutes=6)
    else: # 若已经有了，也往后延五分钟
        reminder_temp += td(minutes=6)
    win_speak('设置为：' + reminder_temp.strftime('%H:%M'))

def clear_temp():
    global reminder_temp
    reminder_temp = END_OF_TIME
    win_speak('已关闭')

keyboard.add_hotkey('ctrl+shift+alt+8', report_next)
keyboard.add_hotkey('ctrl+shift+alt+9', modify_temp)
keyboard.add_hotkey('ctrl+shift+alt+0', clear_temp)
keyboard.add_hotkey('f18', report_next)
keyboard.add_hotkey('f19', modify_temp)
keyboard.add_hotkey('f20', clear_temp)

# === 后台程序 ===============================================

def run_monitors():
    t1 = threading.Thread(target=monitor_config)
    t2 = threading.Thread(target=monitor_time)
    for t in [t1, t2]:
        t.setDaemon(True)
        t.start()



# === 任务图标 ===============================================

from infi.systray import SysTrayIcon

systray = SysTrayIcon("assets\icon.ico", "随静姝个人名师", (
    # ("────────────", None, lambda x: x),
    ("备份", "assets\icon.ico", (
        ("Sound",      "assets\icon.ico",       make_beep),
        ("Speak",      "assets\icon.ico",       say_nihao),
        ("Press",      "assets\icon.ico",       press_key),
    )),
    # ("────────────", None, lambda x: x),
))

# === 开始运行 ===============================================



# keyboard.add_hotkey('ctrl+j', systray.shutdown) # 调试时用的
run_monitors()
systray.start()