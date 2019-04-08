import threading
import ctypes
import ctypes.wintypes
import win32con
from bin import speaker, common

user32 = ctypes.windll.user32  # Windows下的user32.dll


class Hotkey(threading.Thread):  # 通过热键操作某个数值的大小


    HotKeys = {
        # http://www.kbdedit.com/manual/low_level_vk_list.html
        # Ctrl + 0，加10分钟； Ctrl + 5，加5分钟
        100 : (win32con.MOD_CONTROL, win32con.VK_DECIMAL, "+", 0),
        10 : (win32con.MOD_CONTROL, win32con.VK_NUMPAD0, "+", 10*60),
        11 : (win32con.MOD_CONTROL, win32con.VK_NUMPAD1, "+", 1*60),
        12 : (win32con.MOD_CONTROL, win32con.VK_NUMPAD2, "+", 2*60),
        13 : (win32con.MOD_CONTROL, win32con.VK_NUMPAD3, "+", 3*60),
        14 : (win32con.MOD_CONTROL, win32con.VK_NUMPAD4, "+", 4*60),
        15 : (win32con.MOD_CONTROL, win32con.VK_NUMPAD5, "+", 5*60),
        16 : (win32con.MOD_CONTROL, win32con.VK_NUMPAD6, "+", 6*60),
        17 : (win32con.MOD_CONTROL, win32con.VK_NUMPAD7, "+", 7*60),
        18 : (win32con.MOD_CONTROL, win32con.VK_NUMPAD8, "+", 8*60),
        19 : (win32con.MOD_CONTROL, win32con.VK_NUMPAD9, "+", 9*60),

        # Alt + 0，减10分钟； Alt + 5，减5分钟
        200 : (win32con.MOD_ALT, win32con.VK_DECIMAL, "=", 0),
        20 : (win32con.MOD_ALT, win32con.VK_NUMPAD0, "-", 10*60),
        21 : (win32con.MOD_ALT, win32con.VK_NUMPAD1, "-", 1*60),
        22 : (win32con.MOD_ALT, win32con.VK_NUMPAD2, "-", 2*60),
        23 : (win32con.MOD_ALT, win32con.VK_NUMPAD3, "-", 3*60),
        24 : (win32con.MOD_ALT, win32con.VK_NUMPAD4, "-", 4*60),
        25 : (win32con.MOD_ALT, win32con.VK_NUMPAD5, "-", 5*60),
        26 : (win32con.MOD_ALT, win32con.VK_NUMPAD6, "-", 6*60),
        27 : (win32con.MOD_ALT, win32con.VK_NUMPAD7, "-", 7*60),
        28 : (win32con.MOD_ALT, win32con.VK_NUMPAD8, "-", 8*60),
        29 : (win32con.MOD_ALT, win32con.VK_NUMPAD9, "-", 9*60),
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
                if msg.message == win32con.WM_HOTKEY:  # 当监测到有热键被按下时
                    self.handler(msg.wParam)  # msg.wParam 就是热键注册的ID
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageA(ctypes.byref(msg))
        finally:
            self.unregister()