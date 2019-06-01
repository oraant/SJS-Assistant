import threading, time
from bin import common
from bin import speaker
from bin import sentence
from bin import configure
from bin import windows



# 用于追踪并提醒的主要线程
class Tracer(threading.Thread):  # todo: 像hotkey中注册热键
    # todo: 说话、改变量，尽量用语音隔开

    running = False
    elapsed_secs = 0
    shutdown = False

    remind_pattern = {
        'd': [3600, 7200, 18000, 36000],  # 一小时、两小时、五小时、十小时
        'c': [600, 1200, 1800],  # 十分钟、二十分钟、三十分钟
        'b': [60, 120, 180, 240, 300],  # 一分钟、两分钟、三分钟、四分钟、五分钟
        'a': [20, 30],  # 二十秒、三十秒
        's': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 十秒倒计时
    }

    def __init__(self, target_name):
        self.target_name = target_name
        self.target_conf = configure.Targets().configuration[target_name]

        self.frequency = common.str2seconds(self.target_conf['frequency'])  # 监控关键词的频率，防止秒开秒关的情况
        self.trace_gap = common.str2seconds(self.target_conf['trace_gap'])  # 追踪完成后，间隔多少秒重新开始监控
        self.start_lag = common.str2seconds(self.target_conf['start_lag'])  # 播放后的延迟启动时间，保证播放完启动语音

        self.bomb_name = configure.Bombs().pick_item()[0]

        super().__init__()

    def run(self):

        self.trace_welcome()

        while True:
            if self.shutdown:
                break

            if not self.check_start():
                time.sleep(self.frequency)
                continue

            self.trace_start()

            while True:
                if self.check_stop():
                    self.trace_stop()
                    break

                self.trace_remind()

                if self.check_finish():
                    self.trace_finish()
                    break

                self.count_down()

        self.trace_shutdown()


    # -----------------------------------

    def trace_welcome(self):
        common.log('开始监控' + self.target_name, 10)
        pass

    def trace_shutdown(self):
        common.log('停止监控' + self.target_name, 10)
        pass

    # -----------------------------------

    def trace_start(self):

        self.running = True
        self.count_secs = common.str2seconds(self.target_conf['count_short'])
        self.elapsed_secs = self.count_secs

        count_detail = common.seconds2str(self.count_secs)
        speaker.speak(sentence.trace_start(self.target_name, self.bomb_name, count_detail))
        time.sleep(20)  # 保证其说完话

    def trace_remind(self):
        for key in self.remind_pattern.keys():
            if self.count_secs in self.remind_pattern[key]:

                count_detail = common.seconds2str(self.count_secs)
                words = sentence.trace_remind(self.target_name, self.bomb_name, self.count_secs, key)
                speaker.speak(words)

    def trace_stop(self):

        count_detail = common.seconds2str(self.count_secs)
        elapsed_detail = common.seconds2str(self.elapsed_secs - self.count_secs)
        trace_gap = common.seconds2str(self.trace_gap)
        speaker.speak(sentence.trace_stop(self.target_name, self.bomb_name, count_detail, elapsed_detail, trace_gap))  # todo: 将形式简化为一个键值对？

        self.running = False
        time.sleep(self.trace_gap)

    def trace_finish(self):

        elapsed_detail = common.seconds2str(self.elapsed_secs)
        trace_gap = common.seconds2str(self.trace_gap)
        speaker.speak(sentence.trace_finish(self.target_name, self.bomb_name, elapsed_detail, trace_gap))

        self.running = False
        time.sleep(self.trace_gap)

    def trace_punish(self):
        pass  # todo

    # -----------------------------------

    def check_start(self):
        titles = windows.fetch_windows_titles()
        if (self.target_name in titles) and (not self.running):
            return True
        else:
            return False

    def check_stop(self):
        titles = windows.fetch_windows_titles()
        if (self.target_name not in titles) and (self.running):
            return True
        else:
            return False

    def check_finish(self):
        if self.count_secs == 0: return True
        else: return False

    def check_punish(self):
        pass

    # -----------------------------------

    def count_down(self):
        time.sleep(1)
        self.count_secs -= 1

    def count_plus(self):
        pass

    def count_minus(self):
        pass

    def count_clear(self):
        pass

    # -----------------------------------

    def shut_down(self):  # 正在进行中的任务不会被shutdown
        self.shutdown = True


# 根据最新配置，判断是否要监控某一目标
def run(gap = 1):

    tracers = {}

    while True:

        targets_conf = configure.Targets().get_config()

        for target_name in targets_conf.keys():

            if (target_name not in tracers.keys()) and (targets_conf[target_name]['active']):
                tracers[target_name] = Tracer(target_name)
                tracers[target_name].setDaemon(True)
                tracers[target_name].start()

            elif (target_name in tracers.keys()) and (not targets_conf[target_name]['active']):
                tracers[target_name].shut_down()
                tracers.pop(target_name)

        time.sleep(gap)