import database

if __name__ == "__main__":
    db = database.DataBase()
    for so_id, so_hash_value in db.query_id_hash_value_from_so():
        for jupyter_hash_clones in db.query_jupyter_id_by_hash_value(so_hash_value):
            for jupyter_id in jupyter_hash_clones:
                db.insert_clone_pair(jupyter_id, so_id, 1)
