import threading, time

# ------------------------------------------------------------------------------------------------------------------

if True: print(1); print(2)
print(3)
if False: print(1); print(2)
print(3)

exit()  # ------------------------------------------------------------------------------------------------------------------

l = []

class C(threading.Thread):
    a = 2

    def add(self):
        self.a += 1

    def cut(self):
        self.a -= 1

    def run(self):
        l.append(self.add)
        l.append(self.cut)

        for i in range(10):
            print(self.a)
            time.sleep(1)

c = C()
c.setDaemon(True)
c.start()

time.sleep(3)
c.a = 10

time.sleep(3)
l[0]()

time.sleep(3)
l[1]()

time.sleep(3)
exit()  # ------------------------------------------------------------------------------------------------------------------

dddd = {
    "aa": "aaaaaa",
    "bb": "bbbbbbbbb",
    "cc": "cccccccccc",
}

for item in dddd:
    print(item, type(item))

exit()  # ------------------------------------------------------------------------------------------------------------------

key = "<asdf>"
d = key.strip("<>")
d.replace("<", "{")
print(key, d)

exit() # ------------------------------------------------------------------------------------------------------------------


print(type("asdf") is str)
print("asdf" is str)
print(type([1,2]) is list)
print([1,2] is dict)
print(type({}) is dict)
print({} is dict)


exit()  # ------------------------------------------------------------------------------------------------------------------



# copy, deep_copy

def a():
    a1 = {
        "aa": "aaaaaa",
        "bb": "bbbbbbbbb",
        "cc": "cccccccccc",
          }
    a2 = "hello"

    def b(p1, p2):
        p1.update({"dd": "ddddddd"})
        print(p1)

        p2 += " world"
        print(p2)

    b(a1, a2)
    print("-------------")
    print(a1)
    print(a2)

a()

exit() # ------------------------------------------------------------------------------------------------------------------


import threading
import win32com.client as wincl
from ruamel.yaml import YAML

yaml = YAML(typ='safe')

with open('../config/sentences.yaml', encoding="utf-8") as f:
    config = yaml.load(f)

print((config))

exit() # ------------------------------------------------------------------------------------------------------------------

a = 1
class C(threading.Thread):
    def run(self):
        global a
        for i in range(10):
            print(a)
            time.sleep(1)

c = C()
c.setDaemon(True)
print("before run")
c.start()
print("after run")
time.sleep(3)
a = 2
print("after change")
time.sleep(3)



exit()  # ------------------------------------------------------------------------------------------------------------------

from bin import windows
from time import sleep

for i in range(10):
    windows.fetch_windows_titles()
    sleep(1)

exit()  # ------------------------------------------------------------------------------------------------------------------

a = 1
def f():
    a = 2
    print(a)
f()
print(a)

exit()  # ------------------------------------------------------------------------------------------------------------------



dd = {
    "item1":"active1",
    "item2":"active2",
    "item3":"active3",
}
ee = {
    "item4":"active4",
    "item5":"active5",
}


dd.update(ee)
print("{item1}, and {item2}".format(**dd))

exit()  # ------------------------------------------------------------------------------------------------------------------


dd = {
    "item1":{"count":0, "active":True},
    "item2":{"count":0, "active":True},
    "item3":{"count":0, "active":True},
}

s = "afasdfasdf {count} asdfasldf {active}"
s = s.format(**dd["item1"])
print(s)


exit()  # ------------------------------------------------------------------------------------------------------------------

dd = {
    "item1":{"count":0, "active":True},
    "item2":{"count":0, "active":True},
    "item3":{"count":0, "active":True},
}
l = {}

print(dd.keys())
for d in dd.keys():
    print(d)
    print(dd[d]["count"])


print('===')
print(dd)
print(l)

exit()  # ------------------------------------------------------------------------------------------------------------------


from bin.configure import TargetsConfiguration
a = TargetsConfiguration().get_config()["守望先锋"]
print(a)


exit()  # ------------------------------------------------------------------------------------------------------------------

import ctypes

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible



def _fetch_titles():

    titles = []

    def _foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True

    EnumWindows(EnumWindowsProc(_foreach_window), 0)

[print(title) for title in titles]

exit()  # ------------------------------------------------------------------------------------------------------------------



import win32gui

win2find = "暴雪"
whnd = win32gui.FindWindowEx(None, None, None, win2find)
if not (whnd == 0):
  print('FOUND!')



exit()  # ------------------------------------------------------------------------------------------------------------------


import os

process_list = os.popen('tasklist /FO "TABLE" /V /FI "STATUS eq RUNNING"').read().strip().split('\n')
for process in process_list:
    print(process)

exit()

# ------------------------------------------------------------------------------------------------------------------



from infi.systray import SysTrayIcon
from bin import conversation
from bin import speaker
from time import sleep
def say_hello():
    print("Hello, World!")
    speaker.speak(conversation.get_conversation())
menu_options = (("Say Hello", None, say_hello),)

with SysTrayIcon("icon.ico", "asdfffffffffffffffff") as systray:
    for item in ['item1', 'item2', 'item3']:
        systray.update(hover_text=item)
        say_hello()

exit()  # ------------------------------------------------------------------------------------------------------------------



from bin import conversation

if True:
    print('t')

if False:
    print('f')

print(conversation.get_conversation())

exit()

# ------------------------------------------------------------------------------------------------------------------


import requests

res = requests.get('http://v.juhe.cn/joke/randJoke.php?key=d0804bdbf991a1faf5b97a9223f9ee1')
print(res)
res = res.json()
print(res)
print(res['result'][0]['content'])
exit()

# ------------------------------------------------------------------------------------------------------------------



import logging

logging.log(logging.FATAL, 'asdf')


exit()
# ------------------------------------------------------------------------------------------------------------------



import random
l = [1,2,3,4,5]
r1 = random.sample(l, 3)
r2 = random.sample(l, 1)
print(r1)
print(r2)



exit()
# ------------------------------------------------------------------------------------------------------------------

from playsound import playsound
import tempfile
import requests
import time
import threading
import os

url = 'https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts'
data = {
    'voice': 'siyue',
    'appkey': 'isoImgAr3zR2V4Lq',
    'token': '5575a5b2bb5f4b2ba0af0425885d2fc8',
    'format': 'mp3',
    'text': '衍主您好呀',
}
#res = requests.post(url, post=data).content
#url = "https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts";#?appkey=isoImgAr3zR2V4Lq&token=5575a5b2bb5f4b2ba0af0425885d2fc8&format=mp3&voice=siyue&text=一只猪"
res = requests.get(url, params=data).content

print(res)

#playsound(r'C:\Users\oraant\AppData\Local\Temp\tmpszlxm99w.mp3')
#time.sleep(3)
#exit()

def f():
    time.sleep(1)
    print(name4)
    playsound(name4)

with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
    fp.write(res)
    fp.close()
    playsound(fp.name)
    os.remove(fp.name)
    time.sleep(2)

exit()
# ------------------------------------------------------------------------------------------------------------------



from traceback import format_exc as _format_exc

# ------------------------------------------------------------------------------------------------------------------


engine = pyttsx3.init()

speak = wincl.Dispatch("SAPI.SpVoice")
t = threading.Event()


def s(data=""):
    global t
    t.set()
    if data == "": data = """This is a story of two tribal Armenian boys who belonged to the 
         Garoghlanian tribe. """
    s = speak.Speak(data)


t1 = threading.Thread(target=s)

t2 = threading.Thread(target=s, args=("o o o o o o o o o",))
t2.start()
t1.start()

exit()
# ------------------------------------------------------------------------------------------------------------------

import pyttsx3;
engine = pyttsx3.init();
engine.say("I will speak this text");
engine.say("I will speak this text");
engine.runAndWait() ;
engine.stop()

exit()
# ------------------------------------------------------------------------------------------------------------------


import winsound
import win32com.client
import time
import yaml
import random
import threading

speak = win32com.client.Dispatch('SAPI.SPVOICE').Speak

# 公共变量
l = [1,2,3,4,5,6,7,8,9,9]
i = 22

def f(a):
    print(a)

# ------------------------------------------------------------------------------------------------------------------

