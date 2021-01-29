# === 测试功能 ===============================================

import winsound
from win32com.client import Dispatch
win_speak = Dispatch('SAPI.SPVOICE').Speak  # Windows朗读设备，只能阻塞朗读
win_wshshl= Dispatch("WScript.Shell") # 用来发送按键，可以发送组合键

def press_key(systray): win_wshshl.SendKeys('{F13}')
def say_nihao(systray): win_speak('你好')
def make_beep(systray): winsound.Beep(100, 1000)



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

def monitor_config():
    last_position = GetCursorPos()
    while True:
        time.sleep(10)
        count = get_count()
        position = GetCursorPos()

        if count <= 0: continue # 设定触发的必要条件
        if random.random() > 10/3600: continue # 设定触发的概率
        if position == last_position: continue

        press_key(0) # 执行惩罚
        last_position = position
        set_count(count-1)

def run_monitor():
    monitor_thread = threading.Thread(target=monitor_config)
    monitor_thread.setDaemon(True)
    monitor_thread.start()



# === 后台程序 ===============================================

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

run_monitor()
systray.start()