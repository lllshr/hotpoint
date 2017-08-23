import os
import jieba
import jieba.posseg


stop_pos = ('w', 'm', 'q', 'y', 'x', 'u', 'd', 't', 'c', 'mq', 'f', 'z', 'o', 'e', 'p', 'uj', 'df', 'r',
                         'ad', 'ud', 'ns', 's', 'l', 'a', 'nr', 'nz')


class TextProcessing(object):
    def __init__(self, new_path='', stop_path=''):
        self.stopwords = set()
        if len(new_path):
            jieba.load_userdict(new_path)
        if len(stop_path):
            with open(stop_path, 'r', encoding='utf-8-sig') as f:
                self.stopwords = set(word.strip() for word in f.readlines())

    def loadDir(self, dir_name, seg=False, stop=False, type='all'):
        '''
        加载路径内的文档
        :param dir_name:文件夹路径
        :param seg: 是否分词
        :param stop: 是否去停止词
        :param type: all：加载全部文本，custom:仅加载客户的话 server:仅加载坐席的话
        :return:
        '''
        data_dic = {}
        n_processed = 0  # 已处理文本数
        file_list = os.listdir(dir_name)
        for file_name in file_list:
            n_processed += 1
            data_dic[file_name] = self.loadFile('\\'.join([dir_name, file_name]), seg, stop, type)
            if n_processed % 100 == 0:
                print('已处理%d篇文本' % n_processed)
        return data_dic

    def loadFile(self, file_name, seg=False, stop=False, type='all'):
        with open(file_name, 'r', encoding='utf-8-sig') as file:
            # text = ''.join([line.strip().strip('客户：').strip('坐席：') for line in file.readlines()])
            if type == 'all':
                text = ''.join([line.strip() for line in file.readlines()])
            elif type == 'custom':
                text = ''.join([line.strip() for line in file.readlines() if line.startswith('客户：')])
            elif type == 'server':
                text = ''.join([line.strip() for line in file.readlines() if line.startswith('坐席：')])
            return self.textprocess(text, seg, stop)

    def textprocess(self, text, seg=False, stop=False):
        if seg:
            if stop:
                word_list = [ob.word for ob in jieba.posseg.cut(text) if self.useless(ob.word, ob.flag) is False]
            else:
                word_list = [ob.word for ob in jieba.posseg.cut(text)]
            return word_list
        else:
            return text

    def useless(self, word, posseg):
        """
        判断词语在算时是否被剔除
        :param word: 词语
        :param posseg: 词性
        :return:
        """
        if word in self.stopwords \
                or posseg in stop_pos or len(word) < 2 \
                or word.endswith(('到', '了', '呢', '吗', '嘛')):
            return True
        return False


if __name__ == '__main__':
    # jieba.load_userdict('newwords.txt')
    # print(list(jieba.cut('我是他是')))
    tp = TextProcessing(new_path=r'D:\Work\004_基于海量语音的客户诉求热点分析\Code\hotpot\newwords.txt',
                   stop_path=r'D:\Work\004_基于海量语音的客户诉求热点分析\Code\hotpot\stopwords.txt')
    data_dic = tp.loadDir(r'D:\Work\003_语义语料库\Data\senti')
    print(data_dic)
    data_dic = tp.loadDir(r'D:\Work\003_语义语料库\Data\senti', seg=True, stop=True)
    print(data_dic)
    print(tp.textprocess('今天晚上停的电', seg=True))





