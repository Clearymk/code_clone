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
                    "from jupyter_code_snippet where id > 5376729"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql)
        return cursor.fetchall()

    def query_id_hash_value_from_so(self):
        query_sql = "select id, hash_value " \
                    "from so_code_snippet"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql)
        return cursor.fetchall()

    def query_id_code_from_so_by_post_id(self, post_id):
        query_sql = "select id, code " \
                    "from so_code_snippet " \
                    "where so_post_id=%s"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql, (post_id,))
        return cursor.fetchall()

    def query_id_code_from_jupyter_by_jupyter_path(self, jupyter_path):
        query_sql = "select id, code " \
                    "from jupyter_code_snippet " \
                    "where jupyter_path=%s"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql, (jupyter_path,))
        return cursor.fetchall()

    def query_by_sql(self, sql):
        query_sql = sql
        cursor = self.mysql.cursor()
        cursor.execute(query_sql)
        return cursor.fetchall()

    def query_by_sql_cursor(self, sql):
        query_sql = sql
        cursor = self.mysql.cursor()
        cursor.execute(query_sql)
        return cursor

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
        self.commit(jupyter_path)

    def insert_so_code_snippet(self, hash_value, code, so_post_id):
        insert_sql = "insert into so_code_snippet (hash_value, code, so_post_id) " \
                     "values (%s, %s, %s)"
        cursor = self.mysql.cursor()
        cursor.execute(insert_sql, (hash_value, code, so_post_id))
        cursor.close()
        self.commit(so_post_id)

    def insert_clone_pair(self, jupyter_code_snippet_id, so_code_snippet_id, clone_type):
        insert_sql = "INSERT INTO clone_pair (jupyter_code_snippet_id, so_code_snippet_id, clone_type) " \
                     "VALUES (%s, %s, %s)"
        cursor = self.mysql.cursor()
        cursor.execute(insert_sql, (jupyter_code_snippet_id, so_code_snippet_id, clone_type))
        cursor.close()
        self.commit(str(jupyter_code_snippet_id) + " " + str(so_code_snippet_id))

    def query_so_id_from_so_group_by_post_id(self):
        query_sql = "select so_post_id " \
                    "from so_code_snippet " \
                    "group by so_post_id"

        cursor = self.mysql.cursor()
        cursor.execute(query_sql)
        return cursor.fetchall()

    def query_clone_pair_contains(self, so_id, jupyter_id):
        query_sql = "select * " \
                    "from clone_pair " \
                    "where jupyter_code_snippet_id = %s " \
                    "and so_code_snippet_id = %s " \
                    "and clone_type = 2"

        cursor = self.mysql.cursor()
        cursor.execute(query_sql, (jupyter_id, so_id))
        return len(cursor.fetchall()) > 0

    def query_jupyter_id_from_jupyter_group_by_jupyter_path(self):
        query_sql = "select jupyter_path " \
                    "from jupyter_code_snippet " \
                    "where id >= 5366231 " \
                    "group by jupyter_path"

        cursor = self.mysql.cursor()
        cursor.execute(query_sql)
        return cursor.fetchall()

    def query_jupyter_id_by_zip_path(self, jupyter_zip_path):
        query_sql = "select id " \
                    "from jupyter_code_snippet " \
                    "where zip_path=%s"

        cursor = self.mysql.cursor()
        cursor.execute(query_sql, (jupyter_zip_path,))
        return cursor.fetchone()

    def query_so_id_by_zip_path(self, so_zip_path):
        query_sql = "select id " \
                    "from so_code_snippet " \
                    "where zip_path=%s"

        cursor = self.mysql.cursor()
        cursor.execute(query_sql, (so_zip_path,))
        return cursor.fetchone()

    def update_zip_path_by_jupyter_id(self, jupyter_id, jupyter_zip_path):
        update_sql = "update jupyter_code_snippet " \
                     "set zip_path = %s " \
                     "where id = %s"
        cursor = self.mysql.cursor()
        cursor.execute(update_sql, (jupyter_zip_path, jupyter_id))
        cursor.close()
        self.commit(str(jupyter_id) + " " + jupyter_zip_path)

    def update_zip_path_by_post_id(self, post_id, so_zip_path):
        update_sql = "update so_code_snippet " \
                     "set zip_path = %s " \
                     "where id = %s"
        cursor = self.mysql.cursor()
        cursor.execute(update_sql, (so_zip_path, post_id))
        cursor.close()
        self.commit(str(post_id) + " " + so_zip_path)

    def delete_clone_pair_by_jupyter_id(self, jupyter_id):
        delete_sql = "delete from jupyter.clone_pair " \
                     "where jupyter_code_snippet_id = %s"
        cursor = self.mysql.cursor()
        cursor.execute(delete_sql, (jupyter_id,))
        cursor.close()
        print("delete clone pair by jupyter id = ", jupyter_id)
        self.mysql.commit()

    def delete_clone_pair_by_so_id(self, so_id):
        delete_sql = "delete from jupyter.clone_pair " \
                     "where so_code_snippet_id = %s"
        cursor = self.mysql.cursor()
        cursor.execute(delete_sql, (so_id,))
        cursor.close()
        print("delete clone pair by so id = ", so_id)
        self.mysql.commit()

    def delete_so_by_so_id(self, so_id):
        delete_sql = "delete from jupyter.so_code_snippet " \
                     "where id = %s"
        cursor = self.mysql.cursor()
        cursor.execute(delete_sql, (so_id,))
        cursor.close()
        print("delete so by so id = ", so_id)
        self.mysql.commit()

    def delete_jupyter_by_jupyter_id(self, jupyter_id):
        delete_sql = "delete from jupyter.jupyter_code_snippet " \
                     "where id = %s"
        cursor = self.mysql.cursor()
        cursor.execute(delete_sql, (jupyter_id,))
        cursor.close()
        print("delete jupyter by jupyter id = ", jupyter_id)
        self.mysql.commit()

    def commit(self, insert_info):
        self.count += 1
        # 当count大于阈值时提交
        if self.count >= 1000:
            self.count = 0
            self.mysql.commit()
            print("success commit")
        print("success info = " + str(insert_info))
