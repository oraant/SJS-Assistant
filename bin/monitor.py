import threading, time
import webbrowser
from functools import partial, wraps
from random import sample

from bin import common
from bin import speaker
from bin import configure
from bin import windows
from bin import hotkeys



# 用于追踪并提醒的主要线程
class Tracer(threading.Thread):

    running = False
    shutdown = False
    abort = False

    count_secs_lock = threading.Semaphore(1)
    count_secs = 0
    elapsed_secs = 0

    remind_pattern = {
        'd': [3600, 7200, 18000, 36000],  # 一小时、两小时、五小时、十小时
        'c': [600, 1200, 1800],  # 十分钟、二十分钟、三十分钟
        'b': [60, 120, 180, 240, 300],  # 一分钟、两分钟、三分钟、四分钟、五分钟
        'a': [20, 30],  # 二十秒、三十秒
        's': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 十秒倒计时
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

        self.trace_welcome()

        while True:
            if self.check_shutdown():
                break

            if not self.check_start():
                time.sleep(self.frequency)
                continue

            self.trace_start()

            while True:
                if self.check_stop():
                    self.trace_stop()
                    break

                if self.check_abort():
                    self.trace_abort()
                    break

                self.trace_remind()

                if self.check_finish():
                    self.trace_finish()
                    break

                self.count_down()

        self.trace_shutdown()

    # -----------------------------------

    def trace_welcome(self):  # 线程开始
        common.log(50, '开始监控' + self.target_name)
        pass

    def trace_shutdown(self):  # 线程结束
        common.log(50, '停止监控' + self.target_name)
        pass

    def trace_start(self):

        self.running = True
        self.shutdown = False
        self.abort = False

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

    def trace_abort(self):

        self.speak('trace_abort', {
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
        return (self.target_name in titles) and (not self.running)

    def check_stop(self):
        titles = windows.fetch_windows_titles()
        return (self.target_name not in titles) and (self.running)

    def check_abort(self):
        return self.abort

    def check_finish(self):
        return self.count_secs <= 0

    def check_punish(self):
        pass

    def check_shutdown(self):
        return self.shutdown

    # -----------------------------------

    def count_safe(func):
        @wraps(func)
        def wrapper(self, *args, **kw):
            self.count_secs_lock.acquire()
            result = func(self, *args, **kw)
            self.count_secs_lock.release()
            return result
        return wrapper

    @count_safe
    def count_down(self):
        time.sleep(1)
        self.count_secs -= 1

    @count_safe
    def count_plus(self, num):
        self.count_secs += num * 60
        self.elapsed_secs += num * 60
        self.speak('plus_minutes', {
            'change_detail': str(num) + '分钟',
            'count_detail': common.seconds2str(self.count_secs),
        })

    @count_safe
    def count_minus(self, num):
        if num * 60 > self.count_secs:
            self.count_secs = 0
            self.elapsed_secs -= self.count_secs
            self.speak('minus_minutes', {
                'change_detail': str(num) + '分钟',
                'count_detail': common.seconds2str(self.count_secs),
            })
            time.sleep(3)
        else:
            self.count_secs -= num * 60
            self.elapsed_secs -= num * 60
            self.speak('minus_minutes', {
                'change_detail': str(num) + '分钟',
                'count_detail': common.seconds2str(self.count_secs),
            })

    @count_safe
    def count_clear(self):  # 会触发trace_finish
        self.count_secs = 0

    # -----------------------------------

    def report_bomb(self):
        self.speak('report_bomb')
    def next_bomb(self):
        self.bomb_name = self.bombs_conf.pick_next()
        self.speak('next_bomb')
    def prev_bomb(self):
        self.bomb_name = self.bombs_conf.pick_prev()
        self.speak('prev_bomb')
    def random_bomb(self):
        self.bomb_name = self.bombs_conf.pick_item()
        self.speak('random_bomb')
    def clear_bomb(self):
        self.bombs_conf.close_switch(self.bomb_name)
        self.speak('clear_bomb')
    def edit_bomb(self):
        webbrowser.open(common.bombs_file)
        self.speak('edit_bomb')

    # -----------------------------------

    def speak(self, conf_key, ext_dict = None):
        pattern = self.sentences_conf.get_sentence(conf_key)
        target_dict = self.targets_conf.get_package(self.target_name)
        bomb_dict = self.bombs_conf.get_package(self.bomb_name)

        pattern_dict = {}
        pattern_dict.update(target_dict)
        pattern_dict.update(bomb_dict)
        if ext_dict: pattern_dict.update(ext_dict)

        formatted = pattern.format(**pattern_dict)
        speaker.speak(formatted)

    def insert_callbacks(self):
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

            # Interact with Bomb
            ['Alt', '.', self.report_bomb], ['Alt', '+', self.next_bomb], ['Alt', '-', self.prev_bomb],
            ['Alt', '*', self.random_bomb], ['Alt', '/', self.clear_bomb], ['Alt', '↵', self.edit_bomb],
        ]

        for (mod, key, func) in maps:
            hotkeys.register(mod, key, func)

    def delete_callbacks(self):
        maps = [
            # Add num minutes
            ['Ctrl', '1'], ['Ctrl', '2'], ['Ctrl', '3'], ['Ctrl', '4'], ['Ctrl', '5'],
            ['Ctrl', '6'], ['Ctrl', '7'], ['Ctrl', '8'], ['Ctrl', '9'], ['Ctrl', '0'],

            # Cut num minutes
            ['Alt', '1'], ['Alt', '2'], ['Alt', '3'], ['Alt', '4'], ['Alt', '5'],
            ['Alt', '6'], ['Alt', '7'], ['Alt', '8'], ['Alt', '9'], ['Alt', '0'],

            # Interact with Bomb
            ['Alt', '.'], ['Alt', '+'], ['Alt', '-'],
            ['Alt', '*'], ['Alt', '/'], ['Alt', '↵'],
        ]

        for (mod, key) in maps:
            hotkeys.cancel(mod, key)

    def abort_tracer(self):
        self.abort = True

    def shutdown_tracer(self):  # 正在追踪中的任务不会被shutdown，只会停止那些还未追踪的监控任务，或已追踪结束的监控任务
        self.shutdown = True

class SuperVisor():

    tracers = {}
    picked = ""

    def __init__(self, gap = 1):
        self.gap = gap
        self.sentences_conf = configure.Sentences()
        self.targets_conf = configure.Targets()

    # 根据最新配置，判断是否要监控某一目标。
    def run(self):

        self.register_shortcuts()

        while True:

            targets_conf = configure.Targets().get_config()

            for target_name in targets_conf.keys():

                # 根据配置，激活新的监控目标
                if (target_name not in self.tracers.keys()) and (targets_conf[target_name]['active']):
                    self.tracers[target_name] = Tracer(target_name)
                    self.tracers[target_name].setDaemon(True)
                    self.tracers[target_name].start()

                # 根据配置，冻结不再需要的监控目标（只能冻结未活跃的任务，正活跃的会自动等其完成后冻结）
                elif (target_name in self.tracers.keys())\
                and (not targets_conf[target_name]['active'])\
                and (not self.tracers[target_name].running):
                    self.tracers[target_name].shutdown_tracer()
                    self.tracers.pop(target_name)

                self.pick_tracer()

            time.sleep(self.gap)

    # ------------------------------------------------------------------------------------------------------------------

    def pick_tracer(self):

        # 若当前选中了追踪器，并且是活跃的，则无需重新选择
        if self.picked and self.tracers[self.picked].running:
            return

        # 否则重新选择最后一个活跃的追踪器
        picked = None
        for tracer_name in self.tracers.keys():
            if self.tracers[tracer_name].running:
                picked = tracer_name

        # 若没有活跃的追踪器，则尝试清除上一个注册的追踪器的热键
        if not picked:
            if self.picked: self.tracers[self.picked].delete_callbacks()
            self.picked = ""
            return

        # 否则选中刚才的选择，并且注册热键
        self.picked = picked
        self.tracers[self.picked].insert_callbacks()

    def speak(self, conf_key, ext_dict = None):

        pattern = self.sentences_conf.get_sentence(conf_key)

        if self.picked: target_dict = self.targets_conf.get_package(self.picked)
        else: target_dict = {}

        pattern_dict = {}
        pattern_dict.update(target_dict)
        if ext_dict: pattern_dict.update(ext_dict)

        formatted = pattern.format(**pattern_dict)
        speaker.speak(formatted)

    def check_running(self):
        for tracer in self.tracers:
            if self.tracers[tracer].running:
                return True
        return False

    def register_shortcuts(self):

        maps = [
            ['Ctrl', '.', self.report_tracer], ['Ctrl', '↵', self.edit_tracer],
            ['Ctrl', '+', self.next_tracer], ['Ctrl', '-', self.prev_tracer],
            ['Ctrl', '*', self.random_tracer], ['Ctrl', '/', self.clear_tracer],
        ]
        for (mod, key, func) in maps:
            hotkeys.register(mod, key, func)

    # ------------------------------------------------------------------------------------------------------------------

    def report_tracer(self):
        if self.picked: self.speak('report_tracer')
        else: self.speak('report_tracer_empty')

    def next_tracer(self):
        if not self.check_running():
            self.speak('report_tracer_empty')
            return

        picked = self.picked
        while True:
            prev, cur, next = common.search_index(self.tracers, picked)
            picked = list(self.tracers.keys())[next]
            if self.tracers[picked].running: break

        self.picked = picked
        self.tracers[self.picked].insert_callbacks()
        self.speak('next_tracer')

    def prev_tracer(self):
        if not self.check_running():
            self.speak('report_tracer_empty')
            return

        picked = self.picked
        while True:
            prev, cur, next = common.search_index(self.tracers, picked)
            picked = list(self.tracers.keys())[prev]
            if self.tracers[picked].running: break

        self.picked = picked
        self.tracers[self.picked].insert_callbacks()
        self.speak('prev_tracer')

    def random_tracer(self):
        if not self.check_running():
            self.speak('report_tracer_empty')
            return

        picked = self.picked
        while True:
            picked = sample(self.tracers.keys(), 1)[0]
            if self.tracers[picked].running: break

        self.picked = picked
        self.tracers[self.picked].insert_callbacks()
        self.speak('random_tracer')

    def clear_tracer(self):
        if not self.check_running():
            self.speak('report_tracer_empty')
            return

        self.speak('clear_tracer')
        time.sleep(3)  # 保证把话说完
        self.tracers[self.picked].abort_tracer()

    def edit_tracer(self):
        webbrowser.open(common.targets_file)
        self.speak('edit_tracer')

def run():
    sv = SuperVisor()
    sv.run()