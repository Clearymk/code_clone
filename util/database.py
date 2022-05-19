import time
import pymysql


class DataBase(object):
    def __init__(self) -> None:
        self.count = 0
        try:
            self.mysql = pymysql.connect(host='10.19.126.71',
                                         port=3307,
                                         user='root',
                                         password='catlab1a509',
                                         database='jupyter')
        except Exception:
            time.sleep(2)
            self.__init__()

    def query_id_hash_value_from_jupyter(self):
        query_sql = "select id, hash_value " \
                    "from jupyter_code_snippet"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql)
        return cursor.fetchall()

    def query_id_hash_value_from_so(self):
        query_sql = "select id, hash_value " \
                    "from so_code_snippet"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql)
        return cursor.fetchall()

    def query_code_from_so_by_post_id(self, post_id):
        query_sql = "select code " \
                    "from so_code_snippet " \
                    "where so_post_id=%s"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql, (post_id,))
        return cursor.fetchall()

    def query_code_from_jupyter_by_jupyter_path(self, jupyter_path):
        query_sql = "select code " \
                    "from jupyter_code_snippet " \
                    "where jupyter_path=%s"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql, (jupyter_path,))
        return cursor.fetchall()

    def query_so_id_by_hash_value(self, hash_value):
        query_sql = "select id " \
                    "from so_code_snippet " \
                    "where hash_value=%s"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql, (hash_value,))
        return cursor.fetchall()

    def query_jupyter_id_by_hash_value(self, hash_value):
        query_sql = "select id " \
                    "from jupyter_code_snippet " \
                    "where hash_value=%s"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql, (hash_value,))
        return cursor.fetchall()

    def insert_jupyter_code_snippet(self, hash_value, code, jupyter_path):
        insert_sql = "insert into jupyter_code_snippet (hash_value, code, jupyter_path) " \
                     "values (%s, %s, %s)"
        cursor = self.mysql.cursor()
        cursor.execute(insert_sql, (hash_value, code, jupyter_path))
        cursor.close()
        self.commit_insert(jupyter_path)

    def insert_so_code_snippet(self, hash_value, code, so_post_id):
        insert_sql = "insert into so_code_snippet (hash_value, code, so_post_id) " \
                     "values (%s, %s, %s)"
        cursor = self.mysql.cursor()
        cursor.execute(insert_sql, (hash_value, code, so_post_id))
        cursor.close()
        self.commit_insert(so_post_id)

    def insert_clone_pair(self, jupyter_code_snippet_id, so_code_snippet_id, clone_type):
        insert_sql = "INSERT INTO clone_pair (jupyter_code_snippet_id, so_code_snippet_id, clone_type) " \
                     "VALUES (%s, %s, %s)"
        cursor = self.mysql.cursor()
        cursor.execute(insert_sql, (jupyter_code_snippet_id, so_code_snippet_id, clone_type))
        cursor.close()
        self.commit_insert(str(jupyter_code_snippet_id) + " " + str(so_code_snippet_id))

    def query_so_id_from_so_group_by_post_id(self):
        query_sql = "select so_post_id " \
                    "from so_code_snippet " \
                    "group by so_post_id"

        cursor = self.mysql.cursor()
        cursor.execute(query_sql)
        return cursor.fetchall()

    def query_jupyter_id_from_jupyter_group_by_jupyter_path(self):
        query_sql = "select jupyter_path " \
                    "from jupyter_code_snippet " \
                    "group by jupyter_path"

        cursor = self.mysql.cursor()
        cursor.execute(query_sql)
        return cursor.fetchall()

    def commit_insert(self, insert_info):
        self.count += 1
        # 当count大于阈值时提交
        if self.count >= 1:
            self.count = 0
            self.mysql.commit()
        print("insert success insert info = " + str(insert_info))
