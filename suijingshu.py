from bin import configure
from bin import common
from bin import hotkeys
from bin import speaker
import time

# 全局变量

nodes = configure.NodesConfiguration()
words = configure.WordsConfiguration()
shortcuts = hotkeys.Hotkey()
node = ''

# ------ 用户输入 -------------------------------------------------------------------------

# 用户选择节点，或者自己编写新节点，最后将值存放到Node中
def choice_node():
    global node

    while 1:
        tmp_nodes = nodes.pick_items()

        # 展示当前的选项
        remind("\n当前抽取的卡片如下，请用数字选择卡片，回车重新抽取卡片，其他选项请打字输入：")
        for i, v in enumerate(tmp_nodes):
            print("%d - %s" % (i + 1, str(v)))

        # 获取用户的输入
        response = input()
        if response.isdigit():
            choice = int(response)
            node = tmp_nodes[choice-1]
            break
        elif response == "":
            continue
        else:
            node = response
            break

    # 保存用户的选择
    if nodes.search_item(node):
        nodes.add_weight(node)
        remind("节点%s的权重已更改为%d" % (node, nodes.get_weight(node)))
    else:
        remind("自定义节点，无法设置权重")


# 让客户输入倒计时多久，默认三十分钟
def choice_time():
    while 1:  # 暂时还不用加锁，因为快捷键线程还没起
        remind("\n请设置多少分钟后使用此卡片(默认为30分钟)：\n")
        response = input()
        if response == "" : common.seconds = 1800; break
        try:
            common.seconds = common.str2seconds(response)
            break
        except:
            continue
    remind("您将时间设置为%s后\n" % common.seconds2str(common.seconds))


# ------ 计时提醒 -------------------------------------------------------------------------

# 设置不同的有趣的提醒词，并且给提醒者赋予
def remind(node, time = ""):
    if time == "":  # 只说话，不计时。直接指定要说的内容
        print(node)
        speaker.speak(node)
        return
    else:  # 带有计时的说话，需要随机语气
        params = {'node': node, 'time': time}
        statement = words.pick_items(samples=1)[0]
        statement = statement.format(**params)
        print(statement)
        speaker.speak(statement)

# 在不同的时间段，提醒不同的内容
def checkpoint():
    seconds = common.seconds
    if seconds == 7200:
        remind(node, "两个小时")
    if seconds == 3600:
        remind(node, "一个小时")
    if seconds == 1800:
        remind(node, "30分钟")
    if seconds == 1200:
        remind(node, "20分钟")
    if seconds == 600:
        remind(node, "10分钟")
    if seconds == 300:
        remind(node, "5分钟")
    if seconds == 180:
        remind(node, "3分钟")
    if seconds == 120:
        remind(node, "2分钟")
    if seconds == 60:
        remind(node, "1分钟")
    if seconds == 30:
        remind(node, "30秒")
    if seconds == 20:
        remind(node, "20秒")
    if seconds == 10:
        remind("只剩十秒啦，快要倒计时喽")
    if seconds == 5:
        remind("5！")
    if seconds == 4:
        remind("4！")
    if seconds == 3:
        remind("3！")
    if seconds == 2:
        remind("2！")
    if seconds == 1:
        remind("1！")
    if seconds == 0:
        remind("当当当！时间到啦！快去%s吧！" % node)

# 倒计时，一秒减一次，需要多线程加锁
def countdown():
    common.seconds_sem.acquire()
    while common.seconds >= 0:
        checkpoint()
        common.seconds -= 1
        common.seconds_sem.release()
        time.sleep(1)
        common.seconds_sem.acquire()
    common.seconds_sem.release()

# ------ 正式执行 -------------------------------------------------------------------------


#
remind("衍主好呀，我们又见面啦。")

# 用户输入
choice_node()
choice_time()

# 注册热键
shortcuts.setDaemon(True)
shortcuts.start()

# 计时提醒
countdown()
time.sleep(3)