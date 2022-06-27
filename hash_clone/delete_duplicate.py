from util import database

if __name__ == "__main__":
    db = database.DataBase()
    for jupyter_id, so_id in db.query_by_sql("select "
                                             "jupyter_code_snippet_id, so_code_snippet_id "
                                             "from clone_pair "
                                             "where clone_type=1"):
        clone_pairs = db.query_by_sql("select id "
                                     "from clone_pair "
                                     "where jupyter_code_snippet_id = {} "
                                     "and so_code_snippet_id = {} "
                                     "and clone_type = 1".format(jupyter_id, so_id))
        if len(clone_pairs) > 1:
            for i in range(1, len(clone_pairs)):
                db.delete_clone_pair_by_jupyter_id(clone_pairs[i])

    # db.mysql.commit()
