from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedSeq, CommentedMap
from bin import common
from random import sample

# 重要！本模块下所有的类，所有有关获取配置的函数，都会自动读取最新的配置文件

# 基础的配置类，用于读取、存储、改变相关配置
class Configuration():

    def __init__(self, filename):
        self.filename = filename # 需要在这里指定子类的文件路径
        self.yaml = YAML()
        self.yaml.default_flow_style = False

        common.log(10, self.filename)
        self.configuration = None
        self.load_config()

    # 在实例的变量中存、取配置文件
    def load_config(self):
        with open(self.filename, encoding='utf-8') as f:
            self.configuration = self.yaml.load(f)
            common.log(10, self.configuration)

    def save_config(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            self.yaml.dump(self.configuration, f)

    # 返回给别人当前配置，或接收并保存配置文件
    def get_config(self):
        self.load_config()
        return self.configuration

    def set_config(self, config):
        self.configuration = config
        self.save_config()

    # 查找配置表中有无某一项
    def search_item(self, item):
        self.load_config()
        return item in self.configuration.keys()


# 针对列表的配置类，提供了开关、权重、随机抽取等功能
class WeightList(Configuration):

    picked_key = ""

    # ----------------------------------------------
    # 从配置表中，按照一定规则，随机抽取一部分内容

    def check_active(self):
        self.load_config()
        for key in self.configuration.keys():
            if self.configuration[key]['active']:
                return True
        return False

    def pick_items(self, samples=3, weight=True, switch=True):
        if not self.check_active():
            common.log(40, "该配置文件中没有活跃的配置：配置文件:%s" % (self.filename))
            return

        if samples > len(self.configuration.keys()):
            samples = len(self.configuration.keys())

        tmp = []

        for item in self.configuration:
            name, count, active = item, self.configuration[item]["count"], self.configuration[item]["active"]

            if switch == True and active == False: continue  # 判断是否要根据是否激活来取样

            if weight == True: count += 1  # 判断是否将计数作为权重来取样
            else: count = 1

            for i in range(count):  # 按照权重往临时表里增加内容
                tmp.append(name)

        return sample(tmp, samples)

    def pick_item(self):
        self.picked_key = self.pick_items(samples=1)[0]
        self.add_weight(self.picked_key)
        return self.picked_key

    def pick_next(self):
        if not self.check_active():
            common.log(40, "该配置文件中没有活跃的配置：配置文件:%s" % (self.filename))
            return

        if not self.picked_key: self.pick_item()
        self.cut_weight(self.picked_key)

        picked_key = self.picked_key
        while True:
            prev, cur, next = common.search_index(self.configuration, picked_key)
            picked_key = list(self.configuration.keys())[next]
            if self.configuration[picked_key]['active']: break

        self.picked_key = picked_key
        self.add_weight(self.picked_key)
        return self.picked_key

    def pick_prev(self):
        if not self.check_active():
            common.log(40, "该配置文件中没有活跃的配置：配置文件:%s" % (self.filename))
            return

        if not self.picked_key: self.pick_item()
        self.cut_weight(self.picked_key)

        picked_key = self.picked_key
        while True:
            prev, cur, next = common.search_index(self.configuration, picked_key)
            picked_key = list(self.configuration.keys())[prev]
            if self.configuration[picked_key]['active']: break

        self.picked_key = picked_key
        self.add_weight(self.picked_key)
        return self.picked_key

    def repeat_pick(self):
        if self.picked_key:
            return self.picked_key
        else:
            return "刚刚没有选则炸弹，如何重复呢"


    # ----------------------------------------------
    # 操作某一项的权重

    def get_weight(self, item):
        self.load_config()
        return self.configuration[item]["count"]

    def set_weight(self, item, value):
        if value >= 0:
            self.configuration[item]["count"] = value
        self.save_config()

    def add_weight(self, item, change=1):
        current_count = self.configuration[item]["count"]
        self.set_weight(item, current_count+change)

    def cut_weight(self, item, change=1):
        current_count = self.configuration[item]["count"]
        self.set_weight(item, current_count-change)

    # ----------------------------------------------
    # 操作某一项的开关

    def get_switch(self, item):
        self.load_config()
        return self.configuration[item]["active"]

    def toggle_switch(self, item):
        current_active = self.configuration[item]["active"]
        if current_active:
            self.configuration[item]["active"] = False
        else:
            self.configuration[item]["active"] = True
        self.save_config()

    def set_switch(self, item, value):
        current_active = self.configuration[item]["active"]
        if current_active == value: return
        else: self.toggle_switch(item)

    def open_switch(self, item):
        self.set_switch(item, True)

    def close_switch(self, item):
        self.set_switch(item, False)


# 针对语音的配置类
class Sentence(Configuration):

    sentence = ""

    # 从配置中递归解析语句串
    def parse_config(self, config):
        if type(config) is str:
            return config

        if type(config) is CommentedSeq:
            pickup = sample(config, 1)[0]
            return pickup

        pattern_dict = {}
        for key in config.keys():
            if key == "meta": continue
            pattern_dict[key] = self.parse_config(config[key])

        pattern = sample(config["meta"], 1)[0]
        return pattern.format(**pattern_dict)

    # 每次都会尝试重新读取配置文件，避免改个配置还要重启程序
    def get_sentence(self, item_name):
        self.load_config()

        if self.search_item(item_name):
            item = self.configuration[item_name]
        else:
            return "配置读取错误，找不到‘%s’语句" % (item_name)

        self.sentence = self.parse_config(item)
        self.sentence = self.sentence.replace("<", "{")
        self.sentence = self.sentence.replace(">", "}")
        return self.sentence

    def repeat_sentence(self):
        if self.sentence:
            return self.sentence
        else:
            return "静姝刚才没有说话，为什么要重复呢？"


# 针对表达的配置类
# todo: 未来可能会把sentence、expression两个类，换成一个类，且分成“递归随机挑选”、“递归向上替换”两部分。
#  先把不确定的确定下来，然后直接传递一整个？？
#  这样以后的表达会更灵活、语言会更加顺畅
class Expression(Configuration):

    package = {}

    def get_package(self, item_name):
        self.load_config()

        if self.search_item(item_name):
            item = self.configuration[item_name]
        else:
            return "配置读取错误，找不到‘%s’表达" % (item_name)

        for key in item.keys():
            if key.startswith("<") and key.endswith(">"):
                if type(item[key]) is CommentedSeq:
                    self.package[key.strip("<>")] = sample(item[key], 1)[0]
                elif type(item[key]) is str:
                    self.package[key.strip("<>")] = item[key]

        return self.package

    def repeat_package(self):
        if self.package:
            return self.package
        else:
            return "静姝刚才没有选择组合，为什么要重复呢？"


# ------------------------------------------------------------------------------------------------------------------


# 针对引力炸弹列表的配置类
class Bombs(WeightList, Expression):

    def __init__(self):
        common.log(10, common.bombs_file)
        super().__init__(common.bombs_file)

# 针对报时列表的配置类
class Words(WeightList):

    def __init__(self):
        common.log(10, common.words_file)
        super().__init__(common.words_file)

# 针对监控对象的配置类
class Targets(WeightList, Expression):

    def __init__(self):
        common.log(10, common.targets_file)
        super().__init__(common.targets_file)

# 针对语言的配置类
class Sentences(Sentence):

    def __init__(self):
        common.log(10, common.sentences_file)
        super().__init__(common.sentences_file)