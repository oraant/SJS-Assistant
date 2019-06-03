import requests
from random import sample
from queue import Queue


# 从一言随机获取一句话
def _get_sentence():
    res = requests.get('https://v1.hitokoto.cn/?encode=text')

    if "status" in res.text:
        raise ConnectionError('从“一言”获取内容时，联网失败了')

    return(res.text)


# 从数据聚合随机获取一个笑话（因为有次数限制，且每次获取十条，所以需要一个笑话池）
_jokes = Queue()
def _get_joke():

    if not _jokes.empty():
        return _jokes.get()

    res = requests.get('http://v.juhe.cn/joke/randJoke.php?key=d0804bdbf991a1faf5b97a9223f9ee15').json()
    if res['error_code'] != 0:
        raise ConnectionError('从“聚合”获取内容时，联网失败了')

    for joke in res['result']:
        _jokes.put(joke['content'])
    return _jokes.get()


# 随机选择一种方式发言
def get_conversation():

    # 随机生成本次的优先顺序
    if sample([True, False], 1)[0]:
        funcs = [_get_sentence, _get_joke]
    else:
        funcs = [_get_joke, _get_sentence]

    # 尝试获取内容，若获取失败，则尝试另一种
    content = ""
    try:
        content = funcs[0]()
    except:
        try:
            content = funcs[1]()
        except:
            content = "主人，发起对话失败了哦！"
    finally:
        return content