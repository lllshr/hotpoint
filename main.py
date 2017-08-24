import os
import re
import cx_Oracle
import numpy as np
from assist import textprocessing
import hotword
import event
import fileiter


# DOC_PATH = r'/home/pythonUser/transContent'
DOC_PATH = r'C:\Users\l\Desktop\模型部署\hotpoint\text'
if __name__ == '__main__':
    pat = '(\d{5,})_(\d{4}-\d{2}-\d{2})-(\d{2})-\d{2}-\d{2}_(.*).txt'

    # conn = cx_Oracle.connect('yyfxdb', 'yyfxdb', '10.90.85.24:1621/xe')
    # cursor = conn.cursor()
    conn = None
    cursor = None

    hw = hotword.HotWord()

    eve = event.Event()
    eve.loadmodel()

    for path in os.listdir(DOC_PATH):
        if os.path.isdir(os.path.join(DOC_PATH, path)) and re.match('\d{8}', path):
            trans_file = fileiter.FileIter(os.path.join(DOC_PATH, path))  # 内容列表
            for file in trans_file:
                # print(file[0], file[1])

                desc = re.findall(pat, file[0])
                if desc and len(desc[0]) != 4:
                    continue

                area_no = desc[0][0]
                record_date = desc[0][1]
                record_clock = desc[0][2]
                record_id = desc[0][3]

                word_list = np.array(file[1])
                word_added = []
                for word in word_list:
                    hw.add_word_freq(word, area_no=area_no, sta_clock=record_clock)
                    if word not in word_added:
                        hw.add_word_wkst(word, area_no=area_no, sta_clock=record_clock)
                    word_added.append(word)


                event_code = eve.classify(file[1])
                eve.save2db(record_id, event_code, '', area_no, record_date, record_clock, cursor, conn)
            hotwords = hw.get_hotwords(100)
            hw.save2db(hotwords, path, cursor, conn)
            print(hotwords)
            hw = hotword.HotWord()
    #
    # for path in os.listdir(DOC_PATH):
    #     if os.path.isdir(os.path.join(DOC_PATH, path)) and re.match('\d{4}-\d{2}-\d{2}', path):
    #         corpus = tp.loadDir(DOC_PATH, seg=True, stop=True)
    #         hw = hotword.HotWord()
    #         for area_no_key, area_no_val in corpus.values():
    #             for sta_date_key, sta_date_val in area_no_val.values():
    #                 for sta_clock_key, sta_clock_val in sta_date_val.values():
    #
    #         hot_word = hw.get_hotword(list(corpus.values()), topK=100)
    #         hw.save2db(hot_word, area_no, sta_date, sta_clock, cursor, conn)
    #
    #         for file in os.listdir(os.path.join(DOC_PATH, path)):

    #
    #
    #
    #
    #
    #
    #

    #
    # cursor.close
    # conn.close()