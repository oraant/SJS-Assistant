from ruamel.yaml import YAML
from bin import common
from random import sample

config = []  # todo: 写成一个类，其他的用来继承

class Configuration:

    def __init__(self, filename):
        self.filename = filename # 需要在这里指定子类的文件路径
        self.yaml = YAML(typ='safe')
        self.yaml.default_flow_style = False

        common.log(10, self.filename)
        self.configuration = {}
        self.load_config()


    # 将配置从文件中读取到变量里
    def load_config(self):
        with open(self.filename, encoding='utf-8') as f:
            self.configuration = self.yaml.load(f)
            common.log(10, self.configuration)

    # 将配置从变量中写入到配置文件
    def save_config(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            self.yaml.dump(self.configuration, f)

    # 查找配置表中有无这一项
    def search_item(self, item):
        if item in self.configuration.keys():
            return True
        else:
            return False

    # 从配置表中，按照一定规则，随机抽取一部分内容
    def pick_items(self, samples=3, weight=True, switch=True):

        temp = []

        for item in self.configuration:
            name, count, active = item, self.configuration[item]["count"], self.configuration[item]["active"]

            if switch == True and active == False: continue  # 判断是否要根据是否激活来取样

            if weight == True: count += 1  # 判断是否将计数作为权重来取样
            else: count = 1

            for i in range(count):  # 按照权重往临时表里增加内容
                temp.append(name)

        common.log(10, temp)
        return sample(temp, samples)


    # 改变某项变量的值，并保存至文件
    def change_item(self, item, key, value):
        self.configuration[item][key] = value
        self.save_config()


    # 改变某一项的权重，并保存至文件
    def get_weight(self, item):
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



    # 改变某一项的激活，并保存至文件（若已相同，则不再改变）
    def get_switch(self, item):
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
        self.set_switch(item, True)



class NodesConfiguration(Configuration):

    def __init__(self):
        common.log(10, common.nodes_file)
        super().__init__(common.nodes_file)

class WordsConfiguration(Configuration):

    def __init__(self):
        common.log(10, common.words_file)
        super().__init__(common.words_file)