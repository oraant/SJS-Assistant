from infi.systray import SysTrayIcon
import time, threading

from bin import common
from bin import configure
from bin import hotkeys
from bin import speaker
from bin import conversation
from bin import speaker
from bin import monitor

def say_hello(systray):
    print("Hello, World!")
    speaker.speak(conversation.get_conversation())

def run_monitor():
    monitor_thread = threading.Thread(target=monitor.run)
    monitor_thread.setDaemon(True)
    monitor_thread.start()

def register_shortcuts():
    shortcuts = hotkeys.Hotkey()
    shortcuts.setDaemon(True)
    shortcuts.start()

menu_options = (
    ("Say Hello", "assets\icon.ico", say_hello),
    ("Say Hello", "assets\icon.ico", say_hello),
    ("Test", None, say_hello),
    ("Test", None, (
        ("Say Hello", "assets\icon.ico", say_hello),
        ("Say Hello", "assets\icon.ico", say_hello),
        ("Say Hello", None, say_hello),
    )),
)





register_shortcuts()
run_monitor()

systray = SysTrayIcon("assets\icon.ico", "随静姝个人助理", menu_options)
systray.start()