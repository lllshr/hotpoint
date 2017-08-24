from sklearn.externals import joblib


class Event(object):
    def __init__(self):
        self.class_dic = {}
        with open('swords.txt', 'r', encoding='utf-8-sig') as s:
            self.swords = [line.strip() for line in s.readlines() if len(line) > 0]

    def loadmodel(self, vec='model_save/vec.m', trans='model_save/tfidf.m', model='model_save/rf_gini50.0.m'):
        self.vectorizer = joblib.load(vec)
        self.transformer = joblib.load(trans)
        self.clf = joblib.load(model)

    def classify(self, word_list):
        tfidf = self.transformer.transform(self.vectorizer.transform([' '.join([word for word in word_list])]))
        weight = tfidf.toarray()
        result = self.clf.predict(weight)
        # return self.class_dic.get(result[0])
        return int(result[0])

    def save2db(self, record_id, event_code, focus_q, area_no, record_date, record_clock, cursor, conn):

        sql = "INSERT INTO a_detail VALUES(NULL, '" + record_id + "', " + str(event_code) + ", '" + \
              focus_q + "', " + str(area_no) + ", '" + str(record_date) + "', '" + str(record_clock) + \
              "', NULL, NULL, NULL)"
        print(sql)
        # cursor.execute(sql)
        # conn.commit()