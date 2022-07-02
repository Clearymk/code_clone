from database import DataBase
from code_trimmer import CodeTrimmer

db = DataBase()


def remove_jupyter(jupyter_id):
    clone_pairs = db.query_by_sql("select * "
                                  "from jupyter.clone_pair "
                                  "where jupyter_code_snippet_id = {}".format(jupyter_id))
    if len(clone_pairs) > 0:
        db.delete_clone_pair_by_jupyter_id(jupyter_id)

    db.delete_jupyter_by_jupyter_id(jupyter_id)


def remove_so(so_id):
    clone_pairs = db.query_by_sql("select * "
                                  "from jupyter.clone_pair "
                                  "where so_code_snippet_id = {}".format(so_id))
    if len(clone_pairs) > 0:
        db.delete_clone_pair_by_so_id(so_id)

    db.delete_so_by_so_id(so_id)


cursor = db.query_by_sql_cursor("select id, code from jupyter.jupyter_code_snippet")
row = cursor.fetchone()

while row is not None:
    try:
        jupyter_id = row[0]
        jupyter_code = row[1]
        trimmed_code = CodeTrimmer(jupyter_code).trim_comment()
        if trimmed_code.count("\n") < 4:
            remove_jupyter(jupyter_id)
    except Exception as e:
        print(e)

    row = cursor.fetchone()

cursor = db.query_by_sql_cursor("select id, code from jupyter.so_code_snippet")
row = cursor.fetchone()

while row is not None:
    try:
        so_id = row[0]
        so_code = row[1]
        trimmed_code = CodeTrimmer(so_code).trim_comment()
        if so_code.count("\n") < 4:
            remove_so(so_id)
    except Exception as e:
        print(e)

    row = cursor.fetchone()