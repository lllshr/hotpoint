import difflib
import logging
import jieba
from assist import textprocessing


def init():
    first_dic = {}
    second_dic = {}
    second_dic['供电设备较为外显的故障'] = ['起火','着火','漏油','爆炸','倒塌', '打火', '断线', '冒火']
    second_dic['人身伤亡'] = ['死亡','伤','受伤','死']
    second_dic['强制更改客户购电方式'] = ['费控','先缴费','后用电','先用电','后缴费']

    first_dic['供电设备较为外显的故障'] = '敏感事件'
    first_dic['人身伤亡'] = '敏感事件'
    first_dic['强制更改客户购电方式'] = '敏感事件'

    for t1 in list(second_dic.values()):
        for t2 in t1:
            jieba.add_word(t2)
    return first_dic, second_dic


def method1(doc1, doc2):
    if min(len(doc1), len(set(doc2))) == 0:
        return 0
    else:
        return len(set(doc1).intersection(set(doc2))) / min(len(doc1), len(set(doc2)))
    # return difflib.SequenceMatcher(None, doc1, doc2).quick_ratio()


# 主程序
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# 初始化关键词
first_dic, second_dic = init()
tp = textprocessing.TextProcessing('newwords.txt', 'stopwords.txt')

# 读入数据，返回字典，{文件名：[word1, word2, ....]}
data_dic = tp.loadDir(r'D:\Work\003_语义语料库\Data\posseg', seg=True, stop=True, type='all')


for file, word in data_dic.items():
    max = 0
    second_cla = []
    for second_key, key_word in second_dic.items():
        # ratio = method1(list(set(word)), list(set(key_word)))
        ratio = method1(word, list(set(key_word)))
        if ratio >= max and ratio != 0:
            max = ratio
            second_cla.append(second_key)

    res = [' '.join([file, str(max), cla, first_dic.get(cla)]) for cla in second_cla]
    if len(res) > 0:
        print(res)


# if __name__ == '__main__':
#     # print(init())
#     pass