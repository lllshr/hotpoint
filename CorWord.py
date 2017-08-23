# import mysql
from assist import textprocessing


class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        print (' ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)


class CorWord(object):
    def __init__(self, minSup):
        self.minSup = minSup
        pass

    def get_corword(self, corpus):
        """
        获取关联词语
        :param corpus: 语料集
        :return:
        """
        freqItems = fpGrowth(corpus, minSup=self.minSup)
        # 计算共现工单数
        item_cornum = {}
        for item in freqItems:
            # 不考虑1项集
            if len(item) < 2:
                continue
            cor_num = 0
            for text in corpus:
                if len(set(text).intersection(set(item))) == len(item):
                    cor_num += 1
            item_cornum.setdefault(' '.join(item), 0)
            item_cornum[' '.join(item)] = cor_num
        return item_cornum

    def save2db(self, cor_word, db):
        try:
            sql = ''
            db.insert(sql)
        except Exception as e:
            return str(e)


def createTree(dataSet, minSup=1):
    ''' 创建FP树 '''
    # 第一次遍历数据集，创建头指针表
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    # 移除不满足最小支持度的元素项
    temp = {}
    for k in headerTable.keys():
        if headerTable[k] >= minSup:
            temp[k] = headerTable[k]
    headerTable = temp
    # 空元素集，返回空
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None, None
    # 增加一个数据项，用于存放指向相似元素项指针
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    retTree = treeNode('Null Set', 1, None) # 根节点
    # 第二次遍历数据集，创建FP树
    for tranSet, count in dataSet.items():
        localD = {} # 对一个项集tranSet，记录其中每个元素项的全局频率，用于排序
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0] # 注意这个[0]，因为之前加过一个数据项
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)] # 排序
            updateTree(orderedItems, retTree, headerTable, count) # 更新FP树
    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        # 有该元素项时计数值+1
        inTree.children[items[0]].inc(count)
    else:
        # 没有这个元素项时创建一个新节点
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        # 更新头指针表或前一个相似元素项节点的指针指向新节点
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])

    if len(items) > 1:
        # 对剩下的元素项迭代调用updateTree函数
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


# def loadSimpDat():
#     simpDat = [['r', 'z', 'h', 'j', 'p'],
#                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
#                ['z'],
#                ['r', 'x', 'n', 'o', 's'],
#                ['y', 'r', 'x', 'z', 'q', 't', 'p'],
#                ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
#     return simpDat

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict


def findPrefixPath(basePat, treeNode):
    ''' 创建前缀路径 '''
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    if headerTable == None:
        bigL = []
    else:
        bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[0])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minSup)

        if myHead != None:
            # 用于测试
            # print ('conditional tree for:', newFreqSet)
            # myCondTree.disp()

            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)


def fpGrowth(dataSet, minSup=3):
    initSet = createInitSet(dataSet)
    myFPtree, myHeaderTab = createTree(initSet, minSup)
    freqItems = []
    mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItems)
    return freqItems


if __name__ == '__main__':
    tp = textprocessing.TextProcessing(new_path='newwords.txt', stop_path='stopwords.txt')
    f = open('res.txt', 'w', encoding='utf-8-sig')
    # data, data_dic = loaddata.loadData(r'D:\Work\003_语义语料库\Code\Data\test')
    f.write('loadData...\n')
    # print('loadData...')
    # data_dic = loaddata.loadData(r'D:\Work\003_语义语料库\Data\trans')
    data_dic = tp.loadDir(r'D:\Work\003_语义语料库\Data\trans1', seg=True, stop=True)
    # data_dic = loaddata.loadDir(r'D:\Work\003_语义语料库\Code\Data\test', seg=True, stop=True)
    f.write('connect...\n')
    # print('connect...')
    # db = mysql.DbOperation('localhost', 'root', 'liulili', 'hotpot', 3306)
    # dataSet = loaddata.loadDataSet(r'D:\Work\003_语义语料库\Data\trans')
    # print('fpGrowth...')
    f.write('fpGrowth...\n')
    # simpDat = [['r', 'z', 'h', 'j', 'p'],
    #            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
    #            ['z'],
    #            ['r', 'x', 'n', 'o', 's'],
    #            ['y', 'r', 'x', 'z', 'q', 't', 'p'],
    #            ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    # print(list(data_dic.values()))
    minSup = max(100, int(len(data_dic.values())*0.01))
    freqItems = fpGrowth(list(data_dic.values()), minSup=minSup)
    # freqItems = fpGrowth(simpDat, minSup=1)
    # print('loop...')
    f.write('loop...\n')
    for item in freqItems:
        print(item)
        # f.write(item)
        # f.write('\n')
        # cor_num = 0
        # for file, text in data_dic.items():
        #     if len(set(item).intersection(set(text))) == len(item):
        #         cor_num += 1
        # sql = 'INSERT INTO A_CORWORDS VALUES (NULL, ' + str(len(item)) + ', "' + ';'.join(list(item)) + '", ' + str(cor_num/len(data_dic)) + ', NULL);'
        # # db.insert(sql)
        # print(item)
    # db.close()
    f.close()
    # print(freqItems)