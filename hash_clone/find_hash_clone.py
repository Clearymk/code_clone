from util import database

if __name__ == "__main__":
    db = database.DataBase()
    for jupyter_id, jupyter_hash_value in db.query_id_hash_value_from_jupyter():
        for so_hash_clones in db.query_so_id_by_hash_value(jupyter_hash_value):
            for so_id in so_hash_clones:
                if len(db.query_by_sql("select * "
                                       "from clone_pair "
                                       "where clone_type = 1 "
                                       "and jupyter_code_snippet_id={} "
                                       "and so_code_snippet_id ={} ".format(jupyter_id, so_id))) == 0:
                    db.insert_clone_pair(jupyter_id, so_id, 1)
    db.mysql.commit()
