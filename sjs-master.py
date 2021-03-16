# ■■■ 前置功能 ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■



# ━━━ 测试功能 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import winsound
from win32com.client import Dispatch
win_speak = Dispatch('SAPI.SPVOICE').Speak  # Windows朗读设备，只能阻塞朗读
win_speak('随静姝大师开始启动') # 最好先调用一下，不然在线程里调用的时候，容易出现问题。而且还能防止系统哔哔声卡顿
win_wshshl= Dispatch("WScript.Shell") # 用来发送按键，可以发送组合键

def press_key(systray): win_wshshl.SendKeys('{F13}')
def say_nihao(systray): win_speak('你好')
def make_beep(systray): winsound.Beep(1000, 1000)



# ━━━ 读写配置 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from ruamel.yaml import YAML; yaml = YAML()
from bin.common import count_file

def get_count(): # 直接从配置文件中读取count值
    with open(count_file, encoding='utf-8') as f:
        return yaml.load(f)['count']

def set_count(count): # 直接像配置文件中读取count值
    with open(count_file, 'w', encoding='utf-8') as f:
        yaml.dump({'count': count}, f)



# ■■■ 核心功能 ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■



# ━━━ 监控配置文件，并适时执行惩罚 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


import threading, time, random
from win32gui import GetCursorPos
from bin.windows import fetch_windows_titles as winTitles

mc_sleep_gap = 5 # 轮询的间隔，为1就是1秒判断1次
coefficient = 5 # 惩罚的价格，写1就是错1次罚1下，写5就是错1次罚5下
frequency = 10 # 惩罚的频率，若效率、频率都为1，就表示每小时平均惩罚1下

def monitor_config(): # 监控配置文件，若有值，则以一定概率触发惩罚
    last_position = GetCursorPos()
    while True:
        time.sleep(mc_sleep_gap)
        count = get_count()
        position = GetCursorPos()

        if count <= 0: continue # 设定触发的必要条件：必须有数值才行
        if True not in [x in winTitles() for x in ['守望先锋', 'Valheim', 'Nexus', 'bilibili', '知乎']]: continue # 只在犯罪的娱乐时间进行惩罚 # , '', '', '', '', '', '', '', ''
        if random.random() > (mc_sleep_gap * coefficient * frequency)/3600: continue # 设定触发的概率和强度，系数为1时大概1小时吓1次
        if position == last_position: continue

        press_key(0) # 执行惩罚
        last_position = position
        set_count(count-1)

def add_count_to_config(num): # 增加惩罚次数，并提醒
    set_count(get_count()+num*coefficient)
    winsound.Beep(1000, 300)


# ━━━ 自动提醒功能 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from datetime import datetime as dt, time as t, timedelta as td
reminder_list = [
    '00:50', '01:00',
    '01:50', '02:00',
    '02:50', '03:00',
    '03:50', '04:00',
    '04:50', '05:00',
    '05:50', '06:00',
    '06:50', '07:00',
    '07:50', '08:00',
    '08:50', '09:00',
    '13:50', '14:00',
    '19:50', '20:00',
    '22:50', '23:00',
    '23:50', '23:59']
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

def monitor_time(): # 自动报时功能
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
                    win_speak('请注意，时间只有10分钟咯，请10分钟后赶紧特么退出。否则就会被音波灌耳，最好准备哦。')
                if alert_second == 300:
                    win_speak('请注意，时间只剩下5分钟了，请及时退出。准备！准备！准备！5')
                elif alert_second == 1:
                    win_speak('注意！时间到了！请立即矫正自己的行为，否则就要接受音波灌耳的惩罚！警告！警告！十！九！八！七！六！五！四！三！二！一！零！')
                    reminder_temp = END_OF_TIME
                else:
                    win_speak('离%s差%s' % (next_reminder.strftime('%H:%M'), get_delta_str(timedelta)))

# ━━━ 临时计时器功能 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def report_next(): # 报告下一个计时器
    next_reminder = get_reminder()
    speak_content = str(get_count()) + '次。'

    if next_reminder == END_OF_TIME: speak_content += '无闹钟'
    else: speak_content += get_reminder().strftime('%H:%M')

    win_speak(speak_content)

def modify_temp(): # 增加或延后临时计时器
    global reminder_temp
    if reminder_temp == END_OF_TIME: # 若没设置临时闹钟，则设定为当前时间的五分钟后
        reminder_temp = dt.now() + td(minutes=6)
    else: # 若已经有了，也往后延五分钟
        reminder_temp += td(minutes=6)
    win_speak('设置为：' + reminder_temp.strftime('%H:%M'))

def clear_temp(): # 清空临时计时器
    global reminder_temp
    reminder_temp = END_OF_TIME
    win_speak('已关闭')



# ■■■ 主程序入口 ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■



# ━━━ 注册热键 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener

X2ON = False  # 检测X2键是否按下，所有的快捷键只有在X2按下时才生效

def on_mouse_click(x, y, button, pressed): # 通过鼠标中键的状态，开关所有热键功能
    global X2ON
    if str(button) != "Button.middle": return
    if pressed: X2ON = True
    else: X2ON = False
mouse_listener = MouseListener(on_click=on_mouse_click)
mouse_listener.start()


def on_key_press(key): # 实际的热键
    if not X2ON: return

    if str(key) == "Key.esc": clear_temp()
    elif str(key) == "'`'": report_next()
    elif str(key) == "Key.tab": modify_temp()

    elif str(key) == "'1'": add_count_to_config(1)
    elif str(key) == "'2'": add_count_to_config(2)
    elif str(key) == "'3'": add_count_to_config(3)

keyboard_listener = KeyboardListener(on_press=on_key_press)
keyboard_listener.start()



# ━━━ 后台程序 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## def testfunc():
##     for i in range(100):
##         print(X2ON)
##         time.sleep(0.1)
def run_monitors():
    ## targets = [monitor_config, monitor_time, testfunc]
    targets = [monitor_config, monitor_time]

    for target in targets:
        t = threading.Thread(target=target)
        t.setDaemon(True)
        t.start()



# ━━━ 任务图标 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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



# ━━━ 开始运行 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

run_monitors()
systray.start()
## time.sleep(10) # 调试用，10秒钟后自动退出