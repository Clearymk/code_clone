import os.path
import re
import pymysql
import time
import subprocess
import shutil
import stat
import errno
from git import Repo


class DataBase(object):
    def __init__(self) -> None:
        try:
            self.mysql = pymysql.connect(host='10.19.126.71',
                                         port=3307,
                                         user='root',
                                         password='catlab1a509',
                                         database='apks')
        except:
            time.sleep(2)
            self.__init__()


db = DataBase()
download_path = "/media/viewv/Data/jupyter"


def update(git_url, name):
    cur = db.mysql.cursor()
    update_sql = "update jupyter_notebook set is_download = 1 where git_url = '%s'" % (git_url)
    print("update " + name + " to downloaded")
    cur.execute(update_sql)
    db.mysql.commit()


def judge_mode(path, file):
    abs_file = os.path.join(path, file)
    if not os.access(abs_file, os.W_OK):
        os.chmod(abs_file, stat.S_IWOTH)


def handle_remove_read_only(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise


def remove_no_jupyter_file(project_path):
    # remove file not end with .ipynb
    for root, dirs, files in os.walk(project_path):
        if root.find("/.git") != -1:
            continue
        for currentFile in files:
            exts = '.ipynb'
            if not currentFile.lower().endswith(exts):
                os.remove(os.path.join(root, currentFile))
    # remove empty folder
    remove_empty_folders(project_path)


def remove_empty_folders(path, remove_root=True):
    if not os.path.isdir(path):
        return

    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                remove_empty_folders(fullpath)

    files = os.listdir(path)
    if len(files) == 0 and remove_root:
        os.rmdir(path)


if __name__ == "__main__":
    download_range = range(0, 753803)
    os.system("git config --global http.https://github.com.proxy http://127.0.0.1:2340")
    os.system("git config --global https.https://github.com.proxy https://127.0.0.1:2340")
    for jupyter_id in download_range:
        query_sql = "select git_url from jupyter_notebook where id = %d and is_download=0" % (jupyter_id)
        cur = db.mysql.cursor()
        cur.execute(query_sql)
        query_data = cur.fetchone()

        if query_data:
            git_url = query_data[0]
            print(git_url)
            res = re.compile(r"^https://github.com/(?P<owner>.*)/(?P<name>.*).git") \
                .match(git_url) \
                .groupdict()

            owner = res['owner']
            name = res['name']

            save_name = owner + "_" + name

            print("downloading " + save_name)
            save_path = os.path.join(download_path, save_name)

            try:
                if os.path.exists(save_path):
                    shutil.rmtree(save_path, onerror=handle_remove_read_only)
                    time.sleep(1)
                os.mkdir(save_path)
                os.system(
                    "cd " + save_path + "&& git config --global core.protectNTFS false")
                Repo.clone_from("https://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@github.com/%s/%s" % (owner, name),
                                save_path)

                remove_no_jupyter_file(save_path)
                update(git_url, name)
                print("download " + save_name + " finished")
            except Exception as e:
                try:
                    if os.path.exists(save_path):
                        shutil.rmtree(save_path, onerror=handle_remove_read_only)
                        time.sleep(1)
                    print(e)
                except Exception:
                    pass
                with open("log_jupyter.txt", "a") as f:
                    f.write("exception when downloading " + save_name + "\n")
            print("--------")
