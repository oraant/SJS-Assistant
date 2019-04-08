
dd = {
    "item1":{"count":0, "active":True},
    "item2":{"count":0, "active":True},
    "item3":{"count":0, "active":True},
}
l = {}

print(dd.keys())
for d in dd.items():
    print(d)
    print(dd[d]["count"])


print('===')
print(dd)
print(l)

exit()


# ------------------------------------------------------------------------------------------------------------------


dd = {
    "item1":{"count":0, "active":True},
    "item2":{"count":0, "active":True},
    "item3":{"count":0, "active":True},
}

s = "afasdfasdf {count} asdfasldf {active}"
print(dd.items())
s = s.format(**dd["item1"])
print(s)


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

import threading
import win32com.client as wincl
import pyttsx3
from ruamel.yaml import YAML

yaml = YAML(typ='safe')

with open('./words.yaml', encoding="utf-8") as f:
    config = yaml.load(f)

print((config))
exit()

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

