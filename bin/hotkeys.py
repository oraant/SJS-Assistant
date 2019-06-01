import threading
import ctypes
import ctypes.wintypes
from win32con import *
from bin import speaker, common

user32 = ctypes.windll.user32  # Windows下的user32.dll

class Hotkey(threading.Thread):  # 通过热键操作某个数值的大小

    # 热键被调用时默认的方法
    def f(self): common.log("调用了一个未被注册的热键", 20)

    # 热键和方法的绑定映射
    Mapping = {  # http://www.kbdedit.com/manual/low_level_vk_list.html
        MOD_WIN:{
            VK_NUMPAD1: f, VK_NUMPAD2: f, VK_NUMPAD3: f, VK_NUMPAD4: f, VK_NUMPAD5: f,
            VK_NUMPAD6: f, VK_NUMPAD7: f, VK_NUMPAD8: f, VK_NUMPAD9: f, VK_NUMPAD0: f,
            VK_DECIMAL: f, VK_ADD: f, VK_SUBTRACT: f, VK_MULTIPLY: f, VK_DIVIDE: f, VK_RETURN: f,
        },
        MOD_SHIFT: {
            VK_NUMPAD1: f, VK_NUMPAD2: f, VK_NUMPAD3: f, VK_NUMPAD4: f, VK_NUMPAD5: f,
            VK_NUMPAD6: f, VK_NUMPAD7: f, VK_NUMPAD8: f, VK_NUMPAD9: f, VK_NUMPAD0: f,
            VK_DECIMAL: f, VK_ADD: f, VK_SUBTRACT: f, VK_MULTIPLY: f, VK_DIVIDE: f, VK_RETURN: f,
        },
        MOD_CONTROL: {
            VK_NUMPAD1: f, VK_NUMPAD2: f, VK_NUMPAD3: f, VK_NUMPAD4: f, VK_NUMPAD5: f,
            VK_NUMPAD6: f, VK_NUMPAD7: f, VK_NUMPAD8: f, VK_NUMPAD9: f, VK_NUMPAD0: f,
            VK_DECIMAL: f, VK_ADD: f, VK_SUBTRACT: f, VK_MULTIPLY: f, VK_DIVIDE: f, VK_RETURN: f,
        },
        MOD_ALT: {
            VK_NUMPAD1: f, VK_NUMPAD2: f, VK_NUMPAD3: f, VK_NUMPAD4: f, VK_NUMPAD5: f,
            VK_NUMPAD6: f, VK_NUMPAD7: f, VK_NUMPAD8: f, VK_NUMPAD9: f, VK_NUMPAD0: f,
            VK_DECIMAL: f, VK_ADD: f, VK_SUBTRACT: f, VK_MULTIPLY: f, VK_DIVIDE: f, VK_RETURN: f,
        },
    }

    # 当相关热键被按下时，执行相关的命令，并进行相关提示
    def handler(self, id):
        # 获取按下快捷键时，当前剩余的秒数，以及需要进行的操作
        common.seconds_sem.acquire()
        seconds = common.seconds
        operation = self.HotKeys.get(id)[2]
        number = self.HotKeys.get(id)[3]

        # 计算临时变量
        if operation == "+":
            seconds = seconds + number
        elif operation == "-":
            seconds = seconds - number
            if seconds < 0: seconds = 0
        elif operation == "=":
            seconds = number
            if seconds < 0: seconds = 0

        # 更新全局变量
        common.seconds = seconds
        common.seconds_sem.release()

        # 将更新告知用户
        if seconds == 0: return
        if number == 0: statement = "当前时间是："
        else: statement = "时间已改为："
        statement +=  common.seconds2str(seconds)
        print(statement)
        speaker.speak(statement)

    # 批量注册热键
    def register(self):
        for id, (modifier, key, a, b) in self.HotKeys.items():
            if not user32.RegisterHotKey(None, id, modifier, key):
                print("热键： %s + %s 注册失败！" % (modifier, key))

    # 批量取消注册过的热键，必须得释放热键，否则下次就会注册失败
    def unregister(self):
        for id in self.HotKeys.keys():
            user32.UnregisterHotKey(None, id)

    # 线程执行
    def run(self):

        self.register()

        # 循环检测热键是否被按下
        try:
            msg = ctypes.wintypes.MSG()
            while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                if msg.message == WM_HOTKEY:  # 当监测到有热键被按下时
                    self.handler(msg.wParam)  # msg.wParam 就是热键注册的ID
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageA(ctypes.byref(msg))
        finally:
            self.unregister()

def check():
    pass

def listen():
    pass # todo: 热键的启动以后放到这里