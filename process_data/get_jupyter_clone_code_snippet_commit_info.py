import time
from util.proxy import init_proxy

from util.database import DataBase
from find_matched_commit import get_matched_commit
from util.write_log import write_log

if __name__ == "__main__":
    init_proxy()

    db = DataBase()
    # without experience 850779
    for jupyter_code_snippet_id in db.query_by_sql("select distinct jupyter_code_snippet_id "
                                                   "from clone_pair "
                                                   "where jupyter_code_snippet_id > 850779 "
                                                   "order by jupyter_code_snippet_id;"):
        jupyter_code_snippet_id = jupyter_code_snippet_id[0]
        code, jupyter_path = db.query_by_sql("select code, jupyter_path "
                                             "from jupyter_code_snippet "
                                             "where id = {};".format(jupyter_code_snippet_id))[0]
        repo = str(jupyter_path).split("\\")[0].replace("_", "\\", 1)
        file_path = str(jupyter_path)[len(str(jupyter_path).split("\\")[0]) + 1:]

        repo = repo.replace("\\", "/")
        file_path = file_path.replace("\\", "/")

        try:
            sha, author, last_modified, experience = get_matched_commit(code, repo, file_path, token)
            author = "" if not author else author.url
            db.insert_clone_jupyter_snippet_commit(sha, author, last_modified, experience,
                                                   jupyter_code_snippet_id)
            print(jupyter_code_snippet_id)
        except Exception as e:
            time.sleep(5)
            write_log(jupyter_code_snippet_id)
            continue
