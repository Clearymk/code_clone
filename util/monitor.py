import pymysql
import time


class DataBase(object):
    def __init__(self) -> None:
        try:
            self.mysql = pymysql.connect(host='10.19.126.71',
                                         port=3307,
                                         user='root',
                                         password='catlab1a509',
                                         database='jupyter')
        except:
            time.sleep(2)
            self.__init__()

    def query_question_count(self):
        query_sql = "select count(*) from so_code_snippet"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql)
        count = cursor.fetchone()[0]
        cursor.close()
        return count


if __name__ == "__main__":
    prv_count = 0
    while (True):
        db = DataBase()
        cur_count = db.query_question_count()
        print("diff size: " + str(cur_count - prv_count))
        print("total size: " + str(cur_count))
        prv_count = cur_count
        time.sleep(20)
