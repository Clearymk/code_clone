from util.database import DataBase
from find_matched_commit import get_matched_commit

if __name__ == "__main__":
    db = DataBase()
    for jupyter_code_snippet_id in db.query_by_sql("select distinct jupyter_code_snippet_id from clone_pair limit 10;"):
        code, jupyter_path = db.query_by_sql("select code, jupyter_path "
                                             "from jupyter_code_snippet "
                                             "where id = {};".format(jupyter_code_snippet_id[0]))[0]
        repo = str(jupyter_path).split("\\")[0].replace("_", "\\", 1)
        file_path = str(jupyter_path)[len(str(jupyter_path).split("\\")[0]) + 1:]

        repo = repo.replace("\\", "/")
        file_path = file_path.replace("\\", "/")

        commit = get_matched_commit(code, repo, file_path)

        db.insert_clone_jupyter_snippet_commit(commit.sha, commit.author.url, commit.last_modified)
