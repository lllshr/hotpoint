import nltk


class HotWord(object):
    def __init__(self, newpath='newwords.txt'):
        with open(newpath, 'r', encoding='utf-8-sig') as file:
            self.newwords = [word.strip().split()[0] for word in file.readlines() if len(word.strip().split(' ')) > 0]
        self.word_freq = {}
        self.word_wkst = {}
        self.hotwords = {}

    def add_word_freq(self, word, area_no, sta_clock):
        self.word_freq.setdefault(area_no, {})
        self.word_freq[area_no].setdefault(sta_clock, {})
        self.word_freq[area_no][sta_clock].setdefault(word, 0)
        self.word_freq[area_no][sta_clock][word] += 1

    def add_word_wkst(self, word, area_no, sta_clock):
        self.word_wkst.setdefault(area_no, {})
        self.word_wkst[area_no].setdefault(sta_clock, {})
        self.word_wkst[area_no][sta_clock].setdefault(word, 0)
        self.word_wkst[area_no][sta_clock][word] += 1

    def get_hotwords(self, topK=100):
        for area_no, area_no_value in self.word_freq.items():
            order_by_freq = 1
            for sta_clock, word_dic in area_no_value.items():
                word_freq_sort = sorted(word_dic.items(), key=lambda x: x[1], reverse=True)[:min(100, len(word_dic))]
                self.hotwords.setdefault(area_no, {})
                self.hotwords[area_no].setdefault(sta_clock, {})
                for word, freq in word_freq_sort:
                    self.hotwords[area_no][sta_clock].setdefault(word, {})
                    self.hotwords[area_no][sta_clock][word]['order_by_freq'] = order_by_freq
                    self.hotwords[area_no][sta_clock][word]['wordnum'] = freq
                    self.hotwords[area_no][sta_clock][word]['wkstnum'] = self.word_wkst[area_no][sta_clock][word]
                    order_by_freq += 1
        for area_no, area_no_value in self.word_wkst.items():
            order_by_wkst = 1
            for sta_clock, word_dic in area_no_value.items():
                word_wkst_sort = sorted(word_dic.items(), key=lambda x: x[1], reverse=True)[:min(100, len(word_dic))]
                for word, wkst in word_wkst_sort:
                    if word in self.hotwords[area_no][sta_clock].keys():
                        self.hotwords[area_no][sta_clock][word]['order_by_wkst'] = order_by_wkst
                    else:
                        self.hotwords[area_no][sta_clock].setdefault(word, {})
                        self.hotwords[area_no][sta_clock][word]['wordnum'] = self.word_freq[area_no][sta_clock][word]
                        self.hotwords[area_no][sta_clock][word]['wkstnum'] = wkst
                        self.hotwords[area_no][sta_clock][word]['order_by_wkst'] = order_by_wkst
                        word_freq_sort = sorted(word_dic.items(), key=lambda x: x[1], reverse=True)[:min(100, len(word_dic))]
                        order_by_freq = 1
                        for w, freq in word_freq_sort:
                            if w == word:
                                self.hotwords[area_no][sta_clock][word]['order_by_freq'] = order_by_freq
                            else:
                                order_by_freq += 1
                    order_by_wkst += 1
        return self.hotwords

    def save2db(self, hotwords, sta_date, cursor, conn):
        date = sta_date[:4] + '-' + sta_date[4:6] + '-' + sta_date[6:]
        for area_no, area_no_value in self.hotwords.items():
            for sta_clock, word_dic in area_no_value.items():
                for word in word_dic.keys():
                    word_val = self.hotwords[area_no][sta_clock][word]
                    print(type(sta_clock))
                    print(type(date))
                    sql = "INSERT INTO hotpot.a_hotwords VALUES(NULL, '" + word + "', " + \
                  str(word_val['order_by_freq']) + ", " + \
                  str(word_val['order_by_wkst']) + ", " + \
                  str(word_val['wordnum']) + ", " + \
                  str(word_val['wkstnum']) + ", " + str(area_no) + "," + \
                  str(date) + "," + str(sta_clock) + ",NULL, NULL, NULL)"
                print(sql)
                # cursor.execute(sql)
                # conn.commit()