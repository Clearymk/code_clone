from multiprocessing import Queue, Process
from threading import Thread
from util.database import DataBase

urls_queue = Queue()
max_process = 4
scc_result = "scc_result/result.pairs"
file_index = "scc_result/files-stats-0.stats"
so_path = "/home/viewv/Downloads/SourcererCC/tokenizers/file-level/jupyter_so/so_zip"
jupyter_path = "/home/viewv/Downloads/SourcererCC/tokenizers/file-level/jupyter_so/jupyter_zip"
db = DataBase()


def read_clone_pairs():
    with open(scc_result, 'r') as f:
        for clone_pair in f:
            urls_queue.put(clone_pair.strip())

    for i in range(max_process):
        urls_queue.put("DONE")


def process_clone_pair(clone_pair):
    clone_info = clone_pair.strip().split(",")
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
            so_id = db.query_so_id_by_zip_path(src_path[1:-1])[0]
            jupyter_id = db.query_jupyter_id_by_zip_path(dest_path[1:-1])[0]
        else:
            so_id = db.query_jupyter_id_by_zip_path(dest_path[1:-1])[0]
            jupyter_id = db.query_jupyter_id_by_zip_path(src_path[1:-1])[0]
        db.insert_clone_pair(jupyter_id, so_id, 2)


def scc_output_processor():
    print('start send request processor')
    while True:
        url = urls_queue.get()
        if url == "DONE":
            break
        else:
            try:
                process_clone_pair(url)
            except Exception as e:
                print(e)


def main():
    clone_pair_reader_thread = Thread(target=read_clone_pairs)
    clone_pair_reader_thread.start()

    procs = []
    for i in range(max_process):
        p = Process(target=scc_output_processor)
        procs.append(p)
        p.start()

    for p in procs:
        p.join()

    print('all done')
    clone_pair_reader_thread.join()


def init_file_dict(file_dict):
    with open(file_index, "r", encoding="utf8") as f:
        for line in f.readlines():
            file_info = line.strip().split(",")
            file_id = file_info[0] + "," + file_info[1]
            file_path = file_info[2]
            file_dict[file_id] = file_path


if __name__ == '__main__':
    file_dict = {}
    init_file_dict(file_dict)
    main()
