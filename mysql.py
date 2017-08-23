import pymysql
import pymysql.cursors


class DbOperation(object):
    def __init__(self, host, user, psword, db, port):
        try:
            self.connection = None
            self.connection = pymysql.connect(host=host, user=user, password=psword, db=db, port=port, charset='utf8')
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(str(e))
            if self.connection != None:
                self.connection.close()

    def insert(self, sql):
        try:
            with self.connection.cursor() as cursor:
                count = cursor.execute(sql)
                self.connection.commit()
        except Exception as e:
            print(str(e))
            self.connection.close()

    def close(self):
        self.connection.close()
        if self.connection._closed is False:
            self.connection.close()


if __name__ == '__main__':
    db = DbOperation('localhost1', 'root', 'liulili', 'hotpot', 3306)
    db.close()