import win32con
import win32api
import time

# 注意！只为给特殊情况时，高度自定义按键时使用，平常不推荐使用
# 平常推荐直接使用Windows自带的API：  win32com.client.Dispatch("WScript.Shell").SendKeys('^%{HOME}')
# 具体参考：https://docs.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/windows-scripting/8c6yea83(v=vs.84)

# 根据给定的字符，返回对应的键码

alphabet = { # 字母表，win32con 中对所有的键，都有vk_xxx=xxx的键盘码，但唯独把数字和字母给省略掉了，所以需要补上
    "0": 48, "1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55, "8": 56, "9": 57,
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71,
    "H": 72, "I": 73, "J": 74, "K": 75, "L": 76, "M": 77, "N": 78,
    "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90
}

def keycode(char): # 详细的键映射请参考：https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
    up_char = char.upper(); vk_char = 'VK_'+up_char

    if up_char in alphabet: return alphabet[up_char]
    elif hasattr(win32con, vk_char): return getattr(win32con, vk_char)
    else: return 0 # 键码中不存在的值

# 模拟按键反应

def _key_down(vk_code): win32api.keybd_event(vk_code,win32api.MapVirtualKey(vk_code,0),0,0)
def _key_up(vk_code): win32api.keybd_event(vk_code, win32api.MapVirtualKey(vk_code, 0), win32con.KEYEVENTF_KEYUP, 0)

def key_press(key_name): # 点击按键（按下并抬起）
    vk_code = keycode(key_name)
    _key_down(vk_code)
    time.sleep(0.02)
    _key_up(vk_code)