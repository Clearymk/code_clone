import queue
import re
import threading
from util.database import DataBase

log = "log.txt"
so_path = "/media/viewv/Data/jupyter_so/so_zip"
jupyter_path = "/media/viewv/Data/jupyter_so/jupyter_zip"
fail_log = "fail_log.txt"


class Parse(threading.Thread):
    def __init__(self, number, data_list):
        super(Parse, self).__init__()
        self.number = number
        self.data_list = data_list
        self.is_parse = True
        self.db = DataBase()

    def run(self):
        print('starting thread-%d' % self.number)
        while True:
            if self.data_list.qsize() == 0:
                self.is_parse = False
                self.db.mysql.commit()

            if self.is_parse:  # 解析
                try:
                    data = self.data_list.get(timeout=3)
                except Exception as e:
                    data = None
                if data is not None:
                    try:
                        self.parse(data)
                    except Exception as e:
                        print(str(e) + ":" + data + '\n')
                        continue
            else:
                break
        print('退出%d号解析线程' % self.number)

    def parse(self, data):
        clone_info = data.strip().split(":")
        so = jupyter = -1
        src_path = clone_info[0]
        dest_path = clone_info[1]

        if src_path.__contains__(so_path):
            so = 1
        elif src_path.__contains__(jupyter_path):
            jupyter = 1
            if src_path.__contains__("/jupyter_zip_old/"):
                src_path = src_path.replace("/jupyter_zip_old/", "/jupyter_zip/")
                jupyter_project_path = src_path.split("/")[6]
                jupyter_project_path_ex = re.sub(r"_\d.zip", ".zip", jupyter_project_path)
                src_path.replace(jupyter_project_path, jupyter_project_path_ex)

        if dest_path.__contains__(so_path):
            so = 2
        elif dest_path.__contains__(jupyter_path):
            jupyter = 2
            if dest_path.__contains__("/jupyter_zip_old/"):
                dest_path = dest_path.replace("/jupyter_zip_old/", "/jupyter_zip/")
                jupyter_project_path = dest_path.split("/")[6]
                jupyter_project_path_ex = re.sub(r"_\d.zip", ".zip", jupyter_project_path)
                dest_path.replace(jupyter_project_path, jupyter_project_path_ex)

        if so > 0 and jupyter > 0:
            try:
                if so == 1:
                    so_id = self.db.query_so_id_by_zip_path(src_path[1:-1])[0]
                    jupyter_id = self.db.query_jupyter_id_by_zip_path(dest_path[1:-1])[0]
                else:
                    so_id = self.db.query_so_id_by_zip_path(dest_path[1:-1])[0]
                    jupyter_id = self.db.query_jupyter_id_by_zip_path(src_path[1:-1])[0]
            except Exception as e:
                print(e)
                with open(fail_log, "a+", encoding="utf8") as f:
                    f.write(data + "\n")
                return
            print(jupyter_id, so_id, "match !")
            if not self.db.query_clone_pair_contains(so_id, jupyter_id):
                self.db.insert_clone_pair(jupyter_id, so_id, 2)


def read_clone_pairs(data_list, output_file):
    with open(output_file, 'r') as f:
        for clone_pair in f:
            data_list.put(clone_pair.strip())
    return data_list


def main():
    con_parse = 5

    data_list = queue.Queue()
    data_list = read_clone_pairs(data_list, log)
    print("finish loading result pair " + log)

    # 生成N个解析线程
    parse_thread = []
    for i in range(con_parse):
        t = Parse(i + 1, data_list)
        t.start()
        parse_thread.append(t)

    for t in parse_thread:
        t.join()


if __name__ == '__main__':
    main()
