import threading, time
import webbrowser
from functools import partial

from bin import common
from bin import speaker
from bin import configure
from bin import windows
from bin import hotkeys



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
        self.sentences_conf = configure.Sentences()
        self.targets_conf = configure.Targets()
        self.bombs_conf = configure.Bombs()

        self.target_name = target_name
        self.target_conf = self.targets_conf.configuration[target_name]

        self.frequency = common.str2seconds(self.target_conf['frequency'])  # 监控关键词的频率，防止秒开秒关的情况
        self.trace_gap = common.str2seconds(self.target_conf['trace_gap'])  # 追踪完成后，间隔多少秒重新开始监控
        self.start_lag = common.str2seconds(self.target_conf['start_lag'])  # 播放后的延迟启动时间，保证播放完启动语音

        self.bomb_name = self.bombs_conf.pick_item()

        super().__init__()

    def run(self):

        self.register_callback()  # todo: 后期要统一管理，只能有一个注册的
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
        common.log(10, '开始监控' + self.target_name)
        pass

    def trace_shutdown(self):
        common.log(10, '停止监控' + self.target_name)
        pass

    def trace_start(self):

        self.running = True
        self.count_secs = common.str2seconds(self.target_conf['count_short'])
        self.elapsed_secs = self.count_secs

        self.speak('trace_start', {
            'count_detail': common.seconds2str(self.count_secs)
        })

        time.sleep(self.start_lag)  # 保证其说完话

    def trace_remind(self):
        for level in self.remind_pattern.keys():
            if self.count_secs in self.remind_pattern[level]:

                self.speak('trace_remind_' + level, {
                    'count_detail': common.seconds2str(self.count_secs),
                    'count_secs': self.count_secs,
                })

    def trace_stop(self):

        self.speak('trace_stop', {
            'count_detail': common.seconds2str(self.count_secs),
            'elapsed_detail': common.seconds2str(self.elapsed_secs - self.count_secs),
            'trace_gap': common.seconds2str(self.trace_gap),
        })

        self.running = False
        time.sleep(self.trace_gap)

    def trace_finish(self):

        self.speak('trace_finish', {
            'elapsed_detail': common.seconds2str(self.elapsed_secs - self.count_secs),
            'trace_gap': common.seconds2str(self.trace_gap),
        })

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

    def count_plus(self, num):
        self.count_secs += num * 60
        self.elapsed_secs += num * 60
        self.speak('plus_minutes', {
            'change_detail': num + '分钟',
            'count_detail': common.seconds2str(self.count_secs),
        })

    def count_minus(self, num):
        self.count_secs -= num * 60
        self.elapsed_secs -= num * 60
        self.speak('plus_minutes', {
            'change_detail': num + '分钟',
            'count_detail': common.seconds2str(self.count_secs),
        })

    def report_tracer(self):
        pass
    def next_tracer(self):
        pass
    def prev_tracer(self):
        pass
    def random_tracer(self):
        pass
    def clear_tracer(self):
        self.count_secs = 0
        self.elapsed_secs -= self.count_secs
    def edit_tracer(self):
        pass

    def report_bomb(self):
        self.speak('report_bomb', {})
    def next_bomb(self):
        self.bomb_name = self.bombs_conf.pick_next()
        self.speak('next_bomb', {})
    def prev_bomb(self):
        self.bomb_name = self.bombs_conf.pick_prev()
        self.speak('prev_bomb', {})
    def random_bomb(self):
        self.bomb_name = self.bombs_conf.pick_item()
        self.speak('random_bomb', {})
    def clear_bomb(self):
        self.bombs_conf.close_switch(self.bomb_name)
        self.speak('clear_bomb', {})
    def edit_bomb(self):
        webbrowser.open(common.bombs_file)
        self.speak('edit_bomb', {})

    # -----------------------------------

    def register_callback(self):
        cp, cm = self.count_plus, self.count_minus
        cp1, cp2, cp3, cp4, cp5 = partial(cp, 1), partial(cp, 2), partial(cp, 3), partial(cp, 4), partial(cp, 5)
        cp6, cp7, cp8, cp9, cp10 = partial(cp, 6), partial(cp, 7), partial(cp, 8), partial(cp, 9), partial(cp, 10)
        cm1, cm2, cm3, cm4, cm5 = partial(cm, 1), partial(cm, 2), partial(cm, 3), partial(cm, 4), partial(cm, 5)
        cm6, cm7, cm8, cm9, cm10 = partial(cm, 6), partial(cm, 7), partial(cm, 8), partial(cm, 9), partial(cm, 10)

        maps = [
            # Add num minutes
            ['Ctrl', '1', cp1], ['Ctrl', '2', cp2], ['Ctrl', '3', cp3], ['Ctrl', '4', cp4], ['Ctrl', '5', cp5],
            ['Ctrl', '6', cp6], ['Ctrl', '7', cp7], ['Ctrl', '8', cp8], ['Ctrl', '9', cp9], ['Ctrl', '0', cp10],

            # Cut num minutes
            ['Alt', '1', cm1], ['Alt', '2', cm2], ['Alt', '3', cm3], ['Alt', '4', cm4], ['Alt', '5', cm5],
            ['Alt', '6', cm6], ['Alt', '7', cm7], ['Alt', '8', cm8], ['Alt', '9', cm9], ['Alt', '0', cm10],

            # Interact with Tracer
            ['Ctrl', '.', self.report_tracer], ['Ctrl', '+', self.next_tracer], ['Ctrl', '-', self.prev_tracer],
            ['Ctrl', '*', self.random_tracer], ['Ctrl', '/', self.clear_tracer], ['Ctrl', '↵', self.edit_tracer],

            # Interact with Bomb
            ['Alt', '.', self.report_bomb], ['Alt', '+', self.next_bomb], ['Alt', '-', self.prev_bomb],
            ['Alt', '*', self.random_bomb], ['Alt', '/', self.clear_bomb], ['Alt', '↵', self.edit_bomb],
        ]

        for (mod, key, func) in maps:
            hotkeys.register(mod, key, func)

    def speak(self, conf_key, ext_dict):
        pattern = self.sentences_conf.get_sentence(conf_key)
        target_dict = self.targets_conf.get_package(self.target_name)
        bomb_dict = self.bombs_conf.get_package(self.bomb_name)

        pattern_dict = {}
        pattern_dict.update(target_dict)
        pattern_dict.update(bomb_dict)
        pattern_dict.update(ext_dict)

        formatted = pattern.format(**pattern_dict)
        speaker.speak(formatted)

    # -----------------------------------

    def shut_down(self):  # 正在追踪中的任务不会被shutdown，只会停止那些还未追踪的监控任务
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