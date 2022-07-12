import os.path
import shutil
import stat
import errno
from util.download_jupyter import download_repo
from util.database import DataBase
from find_matched_commit import get_matched_commit_from_local


def handle_remove_read_only(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise


if __name__ == "__main__":
    db = DataBase()
    processed_jupyter_id = set()
    low, high, token = input().split()

    for jupyter_code_snippet_id in db.query_by_sql("select distinct jupyter_code_snippet_id "
                                                   "from clone_pair "
                                                   "where jupyter_code_snippet_id not in "
                                                   "(select jupyter_id from clone_jupyter_snippet_commit) "
                                                   "and jupyter_code_snippet_id > {} "
                                                   "and jupyter_code_snippet_id < {};".format(low, high)):
        jupyter_code_snippet_id = jupyter_code_snippet_id[0]
        if jupyter_code_snippet_id in processed_jupyter_id:
            continue

        # 根据jupyter id得到他所在的项目
        jupyter_path = db.query_by_sql("select jupyter_path "
                                       "from jupyter_code_snippet "
                                       "where id = {};".format(jupyter_code_snippet_id))[0][0]
        # 查找相同项目的code snippet
        repo_path_info = jupyter_path.split("\\")[0]
        owner, repo_name = repo_path_info[:repo_path_info.find("_")], repo_path_info[repo_path_info.find("_") + 1:]
        project_task = {jupyter_code_snippet_id}
        for jupyter_id in db.query_by_sql("select distinct id "
                                          "from jupyter_code_snippet "
                                          "where id not in (select jupyter_id from clone_jupyter_snippet_commit) "
                                          "and id in (select jupyter_code_snippet_id from clone_pair)"
                                          "and jupyter_path like '{}%'".format(owner + "_" + repo_name)):
            project_task.add(jupyter_id[0])
        # clone repo
        try:
            download_path = os.path.join("/media/viewv/Data/jupyter", owner + "_" + repo_name)
            download_repo(owner, repo_name, download_path, token)
        except Exception as e:
            print(e)
            continue

        for jupyter_id in project_task:
            code, jupyter_path = db.query_by_sql("select code, jupyter_path "
                                                 "from jupyter_code_snippet "
                                                 "where id = {};".format(jupyter_id))[0]
            file_path = str(jupyter_path)[len(str(jupyter_path).split("\\")[0]) + 1:]
            file_path = file_path.replace("\\", "/")

            try:
                sha, author, last_modified, experience = get_matched_commit_from_local(code, download_path, file_path)
                author = "" if not author else author.name
                db.insert_clone_jupyter_snippet_commit(sha, author, last_modified, experience,
                                                       jupyter_id)
                print(jupyter_id, file_path)
                processed_jupyter_id.add(jupyter_id)
            except Exception as e:
                print(e)
        # 删除下载的repo
        try:
            if os.path.exists(download_path):
                shutil.rmtree(download_path, onerror=handle_remove_read_only)
        except Exception as e:
            print(e)
