from util import database

if __name__ == "__main__":
    db = database.DataBase()
    for jupyter_id, jupyter_hash_value in db.query_id_hash_value_from_jupyter():
        for so_hash_clones in db.query_so_id_by_hash_value(jupyter_hash_value):
            for so_id in so_hash_clones:
                db.insert_clone_pair(jupyter_id, so_id, 1)
