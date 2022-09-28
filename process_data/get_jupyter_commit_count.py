import time
from util.proxy import init_proxy

from util.database import DataBase
from find_matched_commit import get_matched_commit_count
from util.write_log import write_log

if __name__ == "__main__":
    db = DataBase()
    for jupyter_commit_id, jupyter_code_snippet_id, sha in db.query_by_sql("select id,jupyter_id,sha "
                                                                           "from clone_jupyter_snippet_commit "
                                                                           "where experience > 0 "
                                                                           "and id >= 0 and id < 80000"):
        try:
            jupyter_path = db.query_by_sql("select jupyter_path "
                                           "from jupyter_code_snippet "
                                           "where id = {};".format(jupyter_code_snippet_id))[0][0]
            repo = str(jupyter_path).split("\\")[0].replace("_", "\\", 1)
            file_path = str(jupyter_path)[len(str(jupyter_path).split("\\")[0]) + 1:]

            repo = repo.replace("\\", "/")
            commits_count, experience, authors_count = get_matched_commit_count(sha, repo,
                                                                                "")

            if commits_count == -1 and authors_count == -1:
                continue

            db.update_by_sql("update clone_jupyter_snippet_commit "
                             "set commits_count = {}, authors_count={} , experience = {} "
                             "where id = {}".format(commits_count, authors_count, experience, jupyter_commit_id))
            time.sleep(0.5)
        except Exception as e:
            print(e)
