from util.database import DataBase

if __name__ == "__main__":
    scc_result = "/media/viewv/Data/SourcererCC/clone-detector/result.pairs"
    file_index = "scc_result/files-stats-0.stats"
    so_path = "/media/viewv/Data/jupyter_so/so_zip"
    jupyter_path = "/media/viewv/Data/jupyter_so/jupyter_zip"
    db = DataBase()

    file_dict = {}
    with open(file_index, "r", encoding="utf8") as f:
        for line in f.readlines():
            file_info = line.strip().split(",")
            file_id = file_info[0] + "," + file_info[1]
            file_path = file_info[2]
            file_dict[file_id] = file_path
    print("finish loading index file")

    with open(scc_result, "r", encoding="utf8") as f:
        for line in f:
            clone_info = line.strip().split(",")
            so = jupyter = -1
            src_info = clone_info[0] + "," + clone_info[1]
            src_path = file_dict[src_info]

            if src_path.__contains__(so_path):
                so = 1
            elif src_path.__contains__(jupyter_path):
                jupyter = 1

            dest_info = clone_info[2] + "," + clone_info[3]
            dest_path = file_dict[dest_info]

            # print(src_path, dest_path)

            if dest_path.__contains__(so_path):
                so = 2
            elif dest_path.__contains__(jupyter_path):
                jupyter = 2

            if so > 0 and jupyter > 0:
                if so == 1:
                    so_id = db.query_so_id_by_zip_path(src_path[1:-1])[0]
                    jupyter_id = db.query_jupyter_id_by_zip_path(dest_path[1:-1])[0]
                else:
                    so_id = db.query_so_id_by_zip_path(dest_path[1:-1])[0]
                    jupyter_id = db.query_jupyter_id_by_zip_path(src_path[1:-1])[0]
                # print(so_id, jupyter_id)
                if not db.query_clone_pair_contains(so_id, jupyter_id):
                    print(so_id, jupyter_id, "  match")
                    db.insert_clone_pair(jupyter_id, so_id, 2)
            # else:
            #     print(so, jupyter, " do not match")
    db.mysql.commit()
