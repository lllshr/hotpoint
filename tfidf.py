import time
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib
from assist.loaddata import TextProcessing


"""
训练tfidf值并保存
sklearn里面的TF-IDF主要用到了两个函数：CountVectorizer()和TfidfTransformer()。
    CountVectorizer是通过fit_transform函数将文本中的词语转换为词频矩阵。
    矩阵元素weight[i][j] 表示j词在第i个文本下的词频，即各个词语出现的次数。
    通过get_feature_names()可看到所有文本的关键字，通过toarray()可看到词频矩阵的结果。
    TfidfTransformer也有个fit_transform函数，它的作用是计算tf-idf值。
"""


if __name__ == "__main__":
    corpus = [] #文档预料 空格连接

    #读取语料
    print('加载语料...')
    tp = TextProcessing(new_path='newwords.txt', stop_path='stopwords.txt')
    # temp = tp.loadDir(r'D:\Work\003_语义语料库\Data\trans', seg=False, stop=True).values()
    # corpus = [' '.join(text) for text in temp]
    corpus = tp.loadDir(r'D:\Work\003_语义语料库\Data\seg').values()


    #将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()

    #该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()

    print('计算tfidf值...')
    #第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    print('模型保存...')
    joblib.dump(vectorizer, 'model_save/vec.m')
    joblib.dump(transformer, 'model_save/tfidf.m')

    #获取词袋模型中的所有词语
    word = vectorizer.get_feature_names()
    print(word)
    print(len(word))

    #将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
    # weight = tfidf.toarray()
    # vectorizer = joblib.load('model_save/vec.m')
    # word = vectorizer.get_feature_names()

