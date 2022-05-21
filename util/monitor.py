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

    def query_so_count(self):
        query_sql = "select count(*) from so_code_snippet"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql)
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def query_jupyter_count(self):
        query_sql = "select count(*) from jupyter_code_snippet"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql)
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def query_clone_pair_count(self):
        query_sql = "select count(*) from clone_pair"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql)
        count = cursor.fetchone()[0]
        cursor.close()
        return count


if __name__ == "__main__":
    so_prv_count = 0
    jupyter_count = 0
    clone_pair_count = 0

    while True:
        db = DataBase()

        # so_cur_count = db.query_so_count()
        # print("so diff size: " + str(so_cur_count - so_prv_count))
        # print("so total size: " + str(so_cur_count))
        # so_prv_count = so_cur_count
        #
        # jupyter_cur_count = db.query_jupyter_count()
        # print("jupyter diff size: " + str(jupyter_cur_count - jupyter_count))
        # print("jupyter total size: " + str(jupyter_cur_count))
        # jupyter_count = jupyter_cur_count

        clone_pair_cur_count = db.query_jupyter_count()
        print("clone pair diff size: " + str(clone_pair_cur_count - clone_pair_count))
        print("clone pair total size: " + str(clone_pair_cur_count))
        clone_pair_count = clone_pair_cur_count

        print("----------")
        time.sleep(20)
