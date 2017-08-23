import datetime
import nltk
import mysql


'''
返回热词、词频、出现文本数
'''


class HotWord(object):
    def __init__(self, newpath='newwords.txt'):
        with open(newpath, 'r', encoding='utf-8-sig') as file:
            self.newwords = [word.strip().split()[0] for word in file.readlines() if len(word.strip().split(' ')) > 0]

    def get_hotword(self, corpus, topK=100):
        """
        获取热词
        :param corpus: 语料，嵌套列表形式，每个元素为一篇文本的词语列表，形如：[[list1], [list2], ..., [listn]]
        :return:
        """
        # 合并为一个列表
        corpus_word = []  # 所有词语（有可能重复）
        corpus_wkst = []  # 嵌套列表，每个元素为一篇文本的词语列表，但词语不重复
        for text in corpus:
            corpus_word.extend(text)
            corpus_wkst.extend(list(set(text)))

        # 词频矩阵
        freq_dist = nltk.FreqDist(w for w in corpus_word if w in self.newwords)
        freq_common = freq_dist.most_common(topK)
        # 工单频矩阵
        wkst_dist = nltk.FreqDist(w for w in corpus_wkst if w in self.newwords)
        wkst_common = wkst_dist.most_common(topK)

        hotword = {}
        order_by_freq = 1
        # 转为字典形式
        for word, word_num in freq_common:
            hotword.setdefault(word, {})
            hotword[word]['order_by_freq'] = order_by_freq
            hotword[word]['wordnum'] = word_num
            hotword[word]['wkstnum'] = wkst_dist.get(word)
            order_by_freq += 1
        # 补充按工单数排序字段
        order_by_wkst = 1
        for word, wkst_num in wkst_common:
            # 如果词频也在前100位，直接赋值工单排序字段
            if word in hotword.keys():
                hotword[word]['order_by_wkst'] = order_by_wkst
            # 如果词频不在前100位，查找词频排位，并补充工单数排位
            else:
                hotword.setdefault(word, {})
                hotword[word]['order_by_wkst'] = order_by_wkst
                hotword[word]['wordnum'] = freq_dist.get(word)
                hotword[word]['wkstnum'] = wkst_num
                order_by_freq = 1
                for key in freq_dist.keys():
                    if key == word:
                        hotword[word]['order_by_freq'] = order_by_freq
                    else:
                        order_by_freq += 1
            order_by_wkst += 1
        return hotword

    def save2db(self, hot_word, db):
        """
        将热词存储入数据库
        :param hotword: 热词，字典，get_hotword返回的结果
        :param conn:
        :return:
        """
        for word in hot_word:
            sql = "INSERT INTO hotpot.a_hotwords VALUES(NULL, '" + word + "', " + \
                  str(hot_word.get(word)['order_by_freq']) + ", " + \
                  str(hot_word.get(word)['order_by_wkst']) + ", " + \
                  str(hot_word.get(word)['wordnum']) + ", " + \
                  str(hot_word.get(word)['wkstnum']) + ", " + "区域" + "," + \
                  "日期" + "," + "时间" + ",NULL, NULL, NULL);"
            db.insert(sql)
# DOC_PATH = r'D:\Work\003_语义语料库\Data\senti'
#
# starttime = datetime.datetime.now()
#
# print('读取语料...')
# tp = assist.loaddata.TextProcessing('newwords.txt', 'stopwords.txt')
# temp = list(tp.loadDir(DOC_PATH, seg=True, stop=True).values())
# # 合并为一个列表
# corpus_word = []
# corpus_wkst = []
# for text in temp:
#     corpus_word.extend(text)
#     corpus_wkst.extend(list(set(text)))
#
# freq_dist = nltk.FreqDist(w for w in corpus_word)
# freq_common = freq_dist.most_common(100)
# wkst_dist = nltk.FreqDist(w for w in corpus_wkst)
# wkst_common = wkst_dist.most_common(100)
#
# res = {}
# order_by_freq = 1
# for word, word_num in freq_common:
#     res.setdefault(word, {})
#     res[word]['order_by_freq'] = order_by_freq
#     res[word]['wordnum'] = word_num
#     res[word]['wkstnum'] = wkst_dist.get(word)
#     order_by_freq += 1
#
# order_by_wkst = 1
# for word, wkst_num in wkst_common:
#     if word in res.keys():
#         res[word]['order_by_wkst'] = order_by_wkst
#     else:
#         res.setdefault(word, {})
#         res[word]['order_by_wkst'] = order_by_wkst
#         res[word]['wordnum'] = freq_dist.get(word)
#         res[word]['wkstnum'] = wkst_num
#         order_by_freq = 1
#         for key in freq_dist.keys():
#             if key == word:
#                 res[word]['order_by_freq'] = order_by_freq
#             else:
#                 order_by_freq += 1
#     order_by_wkst += 1
#
# print(res)
# endtime = datetime.datetime.now()
# print ('the program run '+str((endtime-starttime).seconds)+' seconds')