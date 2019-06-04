from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from playsound import playsound
from bin import common
import win32com.client
import tempfile
import requests
import json
import time
import os


win_speak = win32com.client.Dispatch('SAPI.SPVOICE').Speak  # Windows朗读设备，只能阻塞朗读


words = ""
expire_time = 0
token = ""
res = b""


# 获取阿里云人工智能语音交互应用的Token。插一句嘴，这是我目前见过的最自然、最悦耳、最甜美、最流畅的TTS服务，关键还是免费的！
def get_token():
    global expire_time
    global token

    # 判断上次获取的Token是否过期（默认一天），没过期就不用重新获取了
    if time.time() < expire_time:
        return token

    # 创建AcsClient实例
    client = AcsClient("LTAIMMXdfV6naBcH", "lvICOgKJOclt3mvTibKKOi36CSJ267", "cn-shanghai")

    # 创建request，并设置参数
    request = CommonRequest()
    request.set_method('POST')
    request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
    request.set_version('2019-02-28')
    request.set_action_name('CreateToken')

    # 获取响应，并将Bytes字符串转换成Python字典
    response = client.do_action_with_exception(request)
    response = json.loads(response)

    # 更新全局变量的相关内容
    expire_time = response["Token"]["ExpireTime"]
    token = response["Token"]["Id"]

# 拿到Token后，联网获取MP3音频数据
def get_mp3():
    global token
    global words
    global res
    data = {
        'voice': common.voice,
        'appkey': common.appkey,
        'format': common.format,
        'token': token,
        'text': words,
    }
    res = requests.get(common.url, params=data).content

# 拿到数据后，将数据写到临时文件中并播放。播放完成后，将该文件删掉
def play_mp3(block = False):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        fp.write(res)
        fp.close()
        playsound(fp.name, block)
        os.remove(fp.name)

# 对外的说话接口
def speak(x, block = False):
    global words
    words = x
    try:
        get_token()
        get_mp3()
        play_mp3(block)
    except:
        win_speak(x)