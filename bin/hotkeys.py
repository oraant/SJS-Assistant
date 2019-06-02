import threading
import ctypes
import ctypes.wintypes
from win32con import *
from bin import common

user32 = ctypes.windll.user32  # Windows下的user32.dll

class Hotkey(threading.Thread):  # 通过热键操作某个数值的大小

    # 管理热键对应的回调函数
    Mapping = {
        # http://www.kbdedit.com/manual/low_level_vk_list.html

        # Win
        100:[MOD_WIN, VK_NUMPAD0, None], 101:[MOD_WIN, VK_NUMPAD1, None], 102:[MOD_WIN, VK_NUMPAD2, None],
        103:[MOD_WIN, VK_NUMPAD3, None], 104:[MOD_WIN, VK_NUMPAD4, None], 105:[MOD_WIN, VK_NUMPAD5, None],
        106:[MOD_WIN, VK_NUMPAD6, None], 107:[MOD_WIN, VK_NUMPAD7, None], 108:[MOD_WIN, VK_NUMPAD8, None],
        109:[MOD_WIN, VK_NUMPAD9, None],

        110:[MOD_WIN, VK_DECIMAL, None], 111:[MOD_WIN, VK_ADD, None], 112:[MOD_WIN, VK_SUBTRACT, None],
        113:[MOD_WIN, VK_MULTIPLY, None], 114:[MOD_WIN, VK_DIVIDE, None], 115:[MOD_WIN, VK_RETURN, None],

        # Shift
        200: [MOD_SHIFT, VK_NUMPAD0, None], 201: [MOD_SHIFT, VK_NUMPAD1, None], 202: [MOD_SHIFT, VK_NUMPAD2, None],
        203: [MOD_SHIFT, VK_NUMPAD3, None], 204: [MOD_SHIFT, VK_NUMPAD4, None], 205: [MOD_SHIFT, VK_NUMPAD5, None],
        206: [MOD_SHIFT, VK_NUMPAD6, None], 207: [MOD_SHIFT, VK_NUMPAD7, None], 208: [MOD_SHIFT, VK_NUMPAD8, None],
        209: [MOD_SHIFT, VK_NUMPAD9, None],

        210: [MOD_SHIFT, VK_DECIMAL, None], 211: [MOD_SHIFT, VK_ADD, None], 212: [MOD_SHIFT, VK_SUBTRACT, None],
        213: [MOD_SHIFT, VK_MULTIPLY, None], 214: [MOD_SHIFT, VK_DIVIDE, None], 215: [MOD_SHIFT, VK_RETURN, None],

        # Control
        300: [MOD_CONTROL, VK_NUMPAD0, None], 301: [MOD_CONTROL, VK_NUMPAD1, None], 302: [MOD_CONTROL, VK_NUMPAD2, None],
        303: [MOD_CONTROL, VK_NUMPAD3, None], 304: [MOD_CONTROL, VK_NUMPAD4, None], 305: [MOD_CONTROL, VK_NUMPAD5, None],
        306: [MOD_CONTROL, VK_NUMPAD6, None], 307: [MOD_CONTROL, VK_NUMPAD7, None], 308: [MOD_CONTROL, VK_NUMPAD8, None],
        309: [MOD_CONTROL, VK_NUMPAD9, None],

        310: [MOD_CONTROL, VK_DECIMAL, None], 311: [MOD_CONTROL, VK_ADD, None], 312: [MOD_CONTROL, VK_SUBTRACT, None],
        313: [MOD_CONTROL, VK_MULTIPLY, None], 314: [MOD_CONTROL, VK_DIVIDE, None], 315: [MOD_CONTROL, VK_RETURN, None],

        # Alt
        400: [MOD_ALT, VK_NUMPAD0, None], 401: [MOD_ALT, VK_NUMPAD1, None], 402: [MOD_ALT, VK_NUMPAD2, None],
        403: [MOD_ALT, VK_NUMPAD3, None], 404: [MOD_ALT, VK_NUMPAD4, None], 405: [MOD_ALT, VK_NUMPAD5, None],
        406: [MOD_ALT, VK_NUMPAD6, None], 407: [MOD_ALT, VK_NUMPAD7, None], 408: [MOD_ALT, VK_NUMPAD8, None],
        409: [MOD_ALT, VK_NUMPAD9, None],

        410: [MOD_ALT, VK_DECIMAL, None], 411: [MOD_ALT, VK_ADD, None], 412: [MOD_ALT, VK_SUBTRACT, None],
        413: [MOD_ALT, VK_MULTIPLY, None], 414: [MOD_ALT, VK_DIVIDE, None], 415: [MOD_ALT, VK_RETURN, None],
    }

    def mapping(self, mod, key, func):
        mod_num = {'Win': 100, 'Shift': 200, 'Ctrl': 300, 'Alt': 400}
        key_num = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '.': 10, '+': 11,
                   '-': 12, '*': 13, '/': 14, '↵': 15}
        map_num = mod_num[mod] + key_num[key]
        print(map_num)
        self.Mapping[map_num][2] = func

    def insert_callback(self, mod, key, func):
        self.mapping(mod, key, func)

    def delete_callback(self, mod, key):
        self.mapping(mod, key, self.f)

    # ------------------------------------------------------------------------------------------------------------------

    # 批量注册热键
    def register(self):
        for id, (modifier, key, func) in self.Mapping.items():
            if not user32.RegisterHotKey(None, id, modifier, key):
                common.log("热键注册失败！ID: %s, MOD: %s, KEY: %s" % (id, modifier, key), 30)

    # 批量取消注册过的热键，必须得释放热键，否则下次就会注册失败
    def unregister(self):
        for id in self.Mapping.keys():
            user32.UnregisterHotKey(None, id)

    # 当对应的热键检测到后
    def handle(self, id):
        f = self.Mapping[id][2]
        if f: f()
        else: common.log("一个未被注册的热键调用了", 20)

    # 循环检测热键是否被触发
    def listener(self):
        msg = ctypes.wintypes.MSG()
        while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
            if msg.message == WM_HOTKEY:  # 当监测到有热键被按下时
                self.handle(msg.wParam)
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageA(ctypes.byref(msg))

    def run(self):
        self.register()
        try:
            self.listener()
        finally:
            self.unregister()

hk = Hotkey()
hk.setDaemon(True)

def listen():
    hk.start()

def register(mod, key, func):
    hk.mapping(mod, key, func)