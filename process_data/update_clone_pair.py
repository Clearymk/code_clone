from util.database import DataBase
from dateutil import parser
from datetime import datetime

db = DataBase()

for jupyter_id, so_id in db.query_by_sql("select jupyter_code_snippet_id, so_code_snippet_id "
                                         "from jupyter.clone_pair where direction = -1;"):
    jupyter_create_date = db.query_by_sql("select commit_date "
                                          "from clone_jupyter_snippet_commit "
                                          "where jupyter_id = {} ".format(jupyter_id))

    so_create_date = db.query_by_sql("select create_date "
                                     "from clone_so_snippet_info "
                                     "where so_id = {}".format(so_id))

    if len(jupyter_create_date) == 0 or len(so_create_date) == 0:
        db.update_by_sql("update clone_pair "
                         "set direction = -1 "
                         "where jupyter_code_snippet_id = {} "
                         "and so_code_snippet_id = {}".format(jupyter_id, so_id))
        continue

    jupyter_create_date = jupyter_create_date[0][0]
    so_create_date = so_create_date[0][0]

    try:
        try:
            jupyter_create_date = parser.parse(jupyter_create_date)
        except:
            jupyter_create_date = datetime.fromtimestamp(int(jupyter_create_date))

        try:
            so_create_date = parser.parse(so_create_date)
        except:
            so_create_date = datetime.fromtimestamp(int(so_create_date))
    except:
        db.update_by_sql("update clone_pair "
                         "set direction = -1 "
                         "where jupyter_code_snippet_id = {} "
                         "and so_code_snippet_id = {}".format(jupyter_id, so_id))
        continue

    jupyter_create_date = jupyter_create_date.replace(tzinfo=None)
    so_create_date = so_create_date.replace(tzinfo=None)

    if jupyter_create_date > so_create_date:
        db.update_by_sql("update clone_pair "
                         "set direction = 1 "
                         "where jupyter_code_snippet_id = {} "
                         "and so_code_snippet_id = {}".format(jupyter_id, so_id))
        print("update jupyter to stackoverflow, jupyter id=" + str(jupyter_id) + " create date =",
              jupyter_create_date,
              "stackoverflow id" + str(so_id) + " create date = ", so_create_date)
    else:
        db.update_by_sql("update clone_pair "
                         "set direction = 2 "
                         "where jupyter_code_snippet_id = {} "
                         "and so_code_snippet_id = {}".format(jupyter_id, so_id))
        print("update stackoverflow to jupyter, jupyter id=" + str(jupyter_id) + " create date =",
              jupyter_create_date,
              "stackoverflow id" + str(so_id) + " create date = ", so_create_date)

db.mysql.commit()