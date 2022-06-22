import queue
import threading
from util.database import DataBase

scc_result = "../res/result.pairs"
file_index = "../res/files-stats-0.stats"
so_path = "/media/viewv/Data/jupyter_so/so_zip"
jupyter_path = "/media/viewv/Data/jupyter_so/jupyter_zip"
file_dict = {}


class Parse(threading.Thread):
    def __init__(self, number, data_list):
        super(Parse, self).__init__()
        self.number = number
        self.data_list = data_list
        self.is_parse = True
        self.db = DataBase()

    def run(self):
        print('启动%d号解析线程' % self.number)
        while True:
            if self.data_list.qsize() == 0:
                self.is_parse = False

            if self.is_parse:  # 解析
                try:
                    data = self.data_list.get(timeout=3)
                except Exception as e:
                    data = None
                if data is not None:
                    try:
                        self.parse(data)
                    except Exception as e:
                        continue
            else:
                break
        print('退出%d号解析线程' % self.number)

    def parse(self, data):
        clone_info = data.strip().split(",")
        so = jupyter = -1
        src_info = clone_info[0] + "," + clone_info[1]
        src_path = file_dict[src_info]

        if src_path.__contains__(so_path):
            so = 1
        elif src_path.__contains__(jupyter_path):
            jupyter = 1

        dest_info = clone_info[2] + "," + clone_info[3]
        dest_path = file_dict[dest_info]

        if dest_path.__contains__(so_path):
            so = 2
        elif dest_path.__contains__(jupyter_path):
            jupyter = 2

        if so > 0 and jupyter > 0:
            if so == 1:
                so_id = self.db.query_so_id_by_zip_path(src_path[1:-1])[0]
                jupyter_id = self.db.query_jupyter_id_by_zip_path(dest_path[1:-1])[0]
            else:
                so_id = self.db.query_jupyter_id_by_zip_path(dest_path[1:-1])[0]
                jupyter_id = self.db.query_jupyter_id_by_zip_path(src_path[1:-1])[0]
            print(jupyter_id, so_id, "match !")
            if not self.db.query_clone_pair_contains(so_id, jupyter_id):
                self.db.insert_clone_pair(jupyter_id, so_id, 2)
        else:
            print(src_path, dest_path, "do not match")


def read_clone_pairs(data_list):
    with open(scc_result, 'r') as f:
        for clone_pair in f:
            data_list.put(clone_pair.strip())
    return data_list


def init_file_index():
    with open(file_index, "r", encoding="utf8") as f:
        for line in f:
            file_info = line.strip().split(",")
            file_id = file_info[0] + "," + file_info[1]
            file_path = file_info[2]
            file_dict[file_id] = file_path


def main():
    con_parse = 3
    init_file_index()
    data_list = queue.Queue()
    data_list = read_clone_pairs(data_list)

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
