# ------------------------------------------------------------------------------------------------------------------
# 将所有窗口的所有标题都抓下来
# Win32 Python: Getting all window titles
# https://sjohannes.wordpress.com/2012/03/23/win32-python-getting-all-window-titles/

import ctypes

# 为繁杂的的调用设置缩写
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible


# 遍历所有系统窗口，并将记录全部标题
def fetch_windows_titles():
    titles = []

    def _foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True

    EnumWindows(EnumWindowsProc(_foreach_window), 0)
    return " ".join(titles)

# ------------------------------------------------------------------------------------------------------------------
# 精确判断某个标题的窗口是否存在，缺点在于窗口标题必须完全匹配，无法做到模糊查询
# Python get specific window title
# https://stackoverflow.com/a/50826897/6324442

from win32gui import FindWindowEx

def check_specific_window(title):
    if FindWindowEx(None, None, None, title) != 0:
        return True
    else:
        return False

# ------------------------------------------------------------------------------------------------------------------
# 利用系统命令抓取所有运行中的进程，缺点在于某些进程的窗口标题是缺失的，比如多个Chrome的某些标签就不显示标题
# Process Monitoring using Python in Windows
# https://mahi130.wordpress.com/2015/08/26/process-monitoring-using-python-in-windows/

import os

def get_process_list():
    system_command = r'tasklist /FO "TABLE" /V /FI "STATUS eq RUNNING"'
    return os.popen(system_command).read().strip().split('\n')