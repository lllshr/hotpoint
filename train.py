import time
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVR
from assist import textprocessing


"""
分类模型训练代码
计算tfidf值
sklearn里面的TF-IDF主要用到了两个函数：CountVectorizer()和TfidfTransformer()。
    CountVectorizer是通过fit_transform函数将文本中的词语转换为词频矩阵。
    矩阵元素weight[i][j] 表示j词在第i个文本下的词频，即各个词语出现的次数。
    通过get_feature_names()可看到所有文本的关键字，通过toarray()可看到词频矩阵的结果。
    TfidfTransformer也有个fit_transform函数，它的作用是计算tf-idf值。
"""

class_dic = {0: '故障报修', 1: '查询电费', 2: '电费发票', 3: '用电密码', 4: '咨询电价', 5: '其它'}


def preprocessing(path, label=0):
    print('读取语料...')
    tp = textprocessing.TextProcessing(new_path='newwords.txt', stop_path='stopwords.txt')
    temp = list(tp.loadDir(path, seg=True, stop=True).values())
    corpus = [' '.join(text) for text in temp]
    lables = np.array(len(corpus)*[label])
    print('共有%d篇语料' % len(corpus))
    return corpus, lables


def getdata(corpus, labels):
    """
    计算文本tfidf值
    :param corpus: 语料库，文本列表，列表中的元素为以空格连接的文本词语
    :param labels: 语料对应的类标签
    :param type: 算法的类型
    :return:
    """
    print('计算tfidf值...')
    # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer(min_df=0.05, max_df=0.95)
    # 该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()

    # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

    print('保存词袋模型...')
    # 保存
    # joblib.dump(vectorizer, 'model_save/vec.m')
    # joblib.dump(transformer, 'model_save/tfidf.m')

    # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
    weight = tfidf.toarray()
    print('划分训练集与测试集...')
    # 划分测试集与训练集
    x_train, x_test, y_train, y_test = train_test_split(weight, labels, test_size=0.1)
    print('训练集%d篇' % len(x_train))
    print('测试集%d篇' % len(x_test))
    return x_train, x_test, y_train, y_test


def train_by_bayes(x_train, x_test, y_train, y_test):
    print('贝叶斯训练...')
    with open('res.txt', 'a', encoding='utf-8-sig') as fout:
        clf = GaussianNB().fit(x_train, y_train)
        joblib.dump(clf, 'model_save/GaussianNB_20170807.m')
        y_test_hat = clf.predict(x_test)  # 测试数据
        result = (y_test_hat == y_test)
        precision = np.mean(result)
        fout.write("高斯贝叶斯\n")
        fout.write('准确率：' + str(precision) + '\n')
        print('准确率：' + str(precision))


def train_by_decisiontree(x_train, x_test, y_train, y_test):
    crite = ['gini', 'entropy']
    with open('res.txt', 'a', encoding='utf-8-sig') as fout:
        for c in crite:
            print('决策树训练_%s...' % c)
            model = DecisionTreeClassifier(criterion=c)
            clf = model.fit(x_train, y_train)
            mode_name = 'model_save/dt_' + c + '.m'
            joblib.dump(clf, mode_name)
            y_test_hat = clf.predict(x_test)  # 测试数据
            result = (y_test_hat == y_test)
            precision = np.mean(result)
            fout.write('决策树_' + c + '\n')
            fout.write('准确率：' + str(precision) + '\n')
            print('准确率：' + str(precision))


def train_by_randomforest(x_train, x_test, y_train, y_test):
    tree_num = np.linspace(10, 100, 19)
    crite = ['gini', 'entropy']
    with open('res.txt', 'a', encoding='utf-8-sig') as fout:
        for c in crite:
            for estimators in tree_num:
                print('随机森林训练_%s_%s...' % (c, str(estimators)))
                clf = RandomForestClassifier(n_estimators=int(estimators), criterion=c, max_depth=3)
                clf.fit(x_train, y_train)
                model_name = 'model_save/rf_' + c + str(estimators) + '.m'
                joblib.dump(clf, model_name)
                y_test_hat = clf.predict(x_test)
                result = (y_test == y_test_hat)
                precision = np.mean(result)
                fout.write('随机森林_' + c + str(estimators) + '\n')
                fout.write('准确率：' + str(precision) + '\n')
                print('准确率：' + str(precision))


def train_by_svm(x_train, x_test, y_train, y_test):
    with open('res.txt', 'a', encoding='utf-8-sig') as fout:
        print('SVR-RBF训练...')
        clf = SVR(kernel='rbf', gamma=0.2, C=100)
        clf = clf.fit(x_train, y_train)
        model_name = 'model_save/svr_rbf_0.2_100.m'
        joblib.dump(clf, model_name)
        y_test_hat = clf.predict(x_test)
        result = (y_test == y_test_hat)
        precision = np.mean(result)
        fout.write('SVR-RBF_0.2_100\n')
        fout.write('准确率：' + str(precision) + '\n')
        print('准确率：' + str(precision))

        print('SVR - Linear训练...')
        clf = SVR(kernel='linear', C=100)
        clf = clf.fit(x_train, y_train)
        model_name = 'model_save/svr_linear_100.m'
        joblib.dump(clf, model_name)
        y_test_hat = clf.predict(x_test)
        result = (y_test == y_test_hat)
        precision = np.mean(result)
        fout.write('SVR-Linear_100\n')
        fout.write('准确率：' + str(precision) + '\n')
        print('准确率：' + str(precision))

        print('SVR - Polynomial训练...')
        clf = SVR(kernel='poly', degree=3, C=100)
        clf = clf.fit(x_train, y_train)
        model_name = 'model_save/svr_poly_3_100.m'
        joblib.dump(clf, model_name)
        y_test_hat = clf.predict(x_test)
        result = (y_test == y_test_hat)
        precision = np.mean(result)
        fout.write('SVR-Linear_3_100\n')
        fout.write('准确率：' + str(precision) + '\n')
        print('准确率：' + str(precision))


if __name__ == "__main__":
    # corpus, labels = preprocessing(r'D:\Work\003_语义语料库\Data\senti')
    TRAIN_PATH = r'D:\Work\003_语义语料库\20170717_语料标注\标注结果-20170814\已完成\train'
    corpus = []
    labels = np.array([])
    for folder in os.listdir(TRAIN_PATH):
        path = os.path.join(TRAIN_PATH, folder)
        if os.path.isdir(path):
            corpus_temp, labels_temp = preprocessing(path, int(folder[:folder.find('_')]))
            corpus.extend(corpus_temp)
            labels = np.concatenate((labels, labels_temp))
    x_train, x_test, y_train, y_test = getdata(corpus, labels)
    train_by_bayes(x_train, x_test, y_train, y_test)
    train_by_decisiontree(x_train, x_test, y_train, y_test)
    train_by_randomforest(x_train, x_test, y_train, y_test)
    train_by_svm(x_train, x_test, y_train, y_test)
