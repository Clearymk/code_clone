import time
import os

from util.database import DataBase
from find_matched_commit import get_matched_commit
from util.write_log import write_log

if __name__ == "__main__":
    os.environ['http_proxy'] = "http://localhost:7890"
    os.environ['HTTP_PROXY'] = "http://localhost:7890"
    os.environ['https_proxy'] = "http://localhost:7890"
    os.environ['HTTPS_PROXY'] = "http://localhost:7890"

    db = DataBase()
    for jupyter_code_snippet_id in db.query_by_sql("select distinct jupyter_code_snippet_id "
                                                   "from clone_pair "
                                                   "where jupyter_code_snippet_id > 49101 "
                                                   "order by jupyter_code_snippet_id;"):
        code, jupyter_path = db.query_by_sql("select code, jupyter_path "
                                             "from jupyter_code_snippet "
                                             "where id = {};".format(jupyter_code_snippet_id[0]))[0]
        repo = str(jupyter_path).split("\\")[0].replace("_", "\\", 1)
        file_path = str(jupyter_path)[len(str(jupyter_path).split("\\")[0]) + 1:]

        repo = repo.replace("\\", "/")
        file_path = file_path.replace("\\", "/")

        try:
            commit = get_matched_commit(code, repo, file_path)
        except Exception as e:
            time.sleep(5)
            write_log(jupyter_code_snippet_id[0])
            continue

        if commit:
            try:
                author = "" if not commit.author else commit.author.url
                db.insert_clone_jupyter_snippet_commit(commit.sha, author, commit.last_modified,
                                                       jupyter_code_snippet_id[0])
                print(jupyter_code_snippet_id[0])
            except Exception as e:
                print(e)
                write_log(jupyter_code_snippet_id[0])
        else:
            write_log(jupyter_code_snippet_id[0])
