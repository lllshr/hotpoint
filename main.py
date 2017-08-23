import os
from sklearn.externals import joblib
from assist import textprocessing
import HotWord
import CorWord
import mysql


DOC_PATH = r'D:\Work\003_语义语料库\20170717_语料标注\标注结果-20170814\已完成\train\1_查询电费'
if __name__ == '__main__':
    class_dic = {}
    with open('event_config.txt', 'r', encoding='utf-8-sig') as config:
        for line in config.readlines():
            if len(line.split(':')) == 2:
                class_dic.setdefault(int(line.split(':')[0]), line.split(':')[1].strip())

    # 读取数据
    print('读取语料...')
    tp = textprocessing.TextProcessing('newwords.txt', 'stopwords.txt')
    corpus = tp.loadDir(DOC_PATH, seg=True, stop=True)
    # 连接数据库
    # db = mysql.DbOperation('localhost', 'root', 'liulili', 'hotpot', 3306)

    # 获取热词
    hw = HotWord.HotWord()
    hot_word = hw.get_hotword(list(corpus.values()), topK=100)
    print(hot_word)
    # 入库存储
    # hw.save2db(hot_word, db)

    # 关联词语
    minSup = max(2, int(len(corpus.values())*0.01))
    cw = CorWord.CorWord(minSup)
    cor_word = cw.get_corword(list(corpus.values()))
    print(cor_word)
    # 入库存储
    # cw.save2db(cor_word, db)

    # 热点
    vectorizer = joblib.load('model_save/vec.m')
    transformer = joblib.load('model_save/tfidf.m')
    clf = joblib.load('model_save/rf_gini50.0.m')
    for file_name in os.listdir(DOC_PATH):
        with open(os.path.join(DOC_PATH, file_name), 'r', encoding='utf-8-sig') as file:
            word_list = tp.textprocess(''.join([line.strip() for line in file.readlines()]), seg=True, stop=True)
            tfidf = transformer.transform(vectorizer.transform([' '.join(word_list)]))
            weight = tfidf.toarray()
            result = clf.predict(weight)
            print(class_dic.get(result[0]))

    # 断开数据库
    # db.close()