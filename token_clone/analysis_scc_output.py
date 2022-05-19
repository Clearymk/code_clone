from util.database import DataBase


if __name__ == "__main__":
    scc_result = "scc_result/result.pairs"
    file_index = "scc_result/files-stats-0.stats"
    so_path = "/home/viewv/Downloads/SourcererCC/tokenizers/file-level/jupyter_so/so_zip"
    jupyter_path = "/home/viewv/Downloads/SourcererCC/tokenizers/file-level/jupyter_so/jupyter_zip"

    file_dict = {}
    with open(file_index, "r", encoding="utf8") as f:
        for line in f.readlines():
            file_info = line.strip().split(",")
            file_id = file_info[0] + "," + file_info[1]
            file_path = file_info[2]
            file_dict[file_id] = file_path

    with open(scc_result, "r", encoding="utf8") as f:
        for line in f.readlines():
            clone_info = line.strip().split(",")
            so = jupyter = False
            src_info = clone_info[0] + "," + clone_info[1]
            src_path = file_dict[src_info]

            if src_path.__contains__(so_path):
                so = True
            elif src_path.__contains__(jupyter_path):
                jupyter = True

            dest_info = clone_info[2] + "," + clone_info[3]
            dest_path = file_dict[dest_info]

            if dest_path.__contains__(so_path):
                so = True
            elif dest_path.__contains__(jupyter_path):
                jupyter = True

            if so and jupyter:
                print(src_path, dest_path)
