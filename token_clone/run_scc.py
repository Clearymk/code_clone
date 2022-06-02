import os
import subprocess
from util.database import DataBase
from zipfile import ZipFile
import os


def write_jupyter_code_into_zip(jupyter_zip_path):
    # max id 5366231
    for jupyter_path in db.query_jupyter_id_from_jupyter_group_by_jupyter_path():
        temp = 1
        jupyter_snippet_id = []

        for jupyter_id, code in db.query_id_code_from_jupyter_by_jupyter_path(jupyter_path[0]):
            # 将查询到的代码写入python文件中
            with open(str(temp) + ".py", "w", encoding="utf8") as f:
                f.write(code)
            jupyter_snippet_id.append(jupyter_id)
            temp += 1
        # 将写入的python文件压缩进一个zip文件中
        # os.path.splitext(jupyter_path[0].split("\\")[-1])[0]
        jupyter_zip_file = writer_into_zip(temp, os.path.splitext(jupyter_path[0].split("\\")[-1])[0], jupyter_zip_path)

        for i in range(1, temp):
            db.update_zip_path_by_jupyter_id(jupyter_snippet_id[i - 1],
                                             os.path.join(jupyter_zip_file, str(i) + ".py"))


def write_so_code_into_zip(so_zip_path):
    for so_post_id in db.query_so_id_from_so_group_by_post_id():
        temp = 1
        so_snippet_id = []

        for so_id, code in db.query_id_code_from_so_by_post_id(so_post_id[0]):
            # 将查询到的代码写入python文件中
            with open(str(temp) + ".py", "w", encoding="utf8") as f:
                f.write(code)
            so_snippet_id.append(so_id)
            temp += 1
        # 将写入的python文件压缩进一个zip文件中, 由于文件名以post_id作为名字，所以不需要移除后缀名
        so_zip_file = writer_into_zip(temp, so_post_id[0], so_zip_path)

        for i in range(1, temp):
            db.update_zip_path_by_post_id(so_snippet_id[i - 1],
                                          os.path.join(so_zip_file, str(i) + ".py"))


def writer_into_zip(file_range, zip_file_name, zip_path):
    if zip_file_name == "":
        print()
    zip_file = os.path.join(zip_path, zip_file_name + ".zip")

    count = 1
    while os.path.exists(zip_file):
        count += 1
        zip_file = os.path.join(zip_path, zip_file_name + "_" + str(count) + ".zip")

    with ZipFile(zip_file, "w") as zf:
        for i in range(1, file_range):
            zf.write(str(i) + ".py")
            # 删除写入的python文件
            os.remove(str(i) + ".py")
    return zip_file

# 将文件地址写入到projects-list
def gen_projects_list(project_path, project_list_path):
    zip_paths = []
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [os.path.join(root, d) for d in dirs]
        files = [fi for fi in files if fi.endswith(".zip")]
        files = [os.path.abspath(os.path.join(root, f)) for f in files]
        if len(files) > 0:
            zip_paths.extend(files)

    with open(os.path.join(project_list_path, "projects-list.txt"), "w", encoding="utf8") as f:
        for zip_path in zip_paths:
            f.write(zip_path + "\n")


# 清除之前运行是留下的历史数据
def cleanup(clean_up_path):
    cleanup_script = subprocess.Popen("cd  " + clean_up_path + " && sh ./cleanup.sh", shell=True,
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(cleanup_script.communicate())
    print(cleanup_script.returncode)


# 生成token
def gen_token(tokenizer_path):
    tokenizer_script = subprocess.Popen("cd  " + tokenizer_path + " && python " + "tokenizer.py",
                                        shell=True,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(tokenizer_script.communicate())
    print(tokenizer_script.returncode)
    # 将生成的token汇总到blocks.file
    export_blocks = subprocess.Popen("cd " + tokenizer_path + "&& cat files_tokens/* > blocks.file",
                                     shell=True,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    export_blocks.wait()


# 生成query_file
def gen_query_file(blocks_path, size):
    cp_script = subprocess.Popen("cd " + blocks_path +
                                 " && python unevensplit.py "
                                 + os.path.join(blocks_path, "blocks.file") + " " + str(size),
                                 shell=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
    cp_script.wait()
    # tokens = []
    # with open(os.path.join(blocks_path, "blocks.file"), "r", encoding="utf8") as f:
    #     for line in f.readlines():
    #         tokens.append(line)
    # k, m = divmod(len(tokens), size)
    # count = 1
    # for query_file in (tokens[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(size)):
    #     with open(os.path.join(blocks_path, "query_{}.file".format(count)), "w", encoding="utf8") as f:
    #         for token in query_file:
    #             f.write(token)
    #     count += 1


# 复制query_file到clone-detector中
def cp_query_file(query_file_path, size):
    for i in range(0, size):
        cp_script = subprocess.Popen("cd " + query_file_path + " && cp "
                                     + "query_{}.file".format(i + 1)
                                     + " ../../clone-detector/",
                                     shell=True,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        cp_script.wait()


# 复制blocks.file到dataset中
def cp_blocks_file(block_file_path):
    cp_script = subprocess.Popen("cd " + block_file_path + " && cp blocks.file ../../clone-detector/input/dataset/",
                                 shell=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
    cp_script.wait()


# 运行查重工具
def run_controller(controller_path):
    run_script = subprocess.Popen("cd " + controller_path + " && python controller.py",
                                  shell=True,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    print(run_script.communicate())
    print(run_script.returncode)


# 导出查重结果
def export_result(detector_path):
    export_script = subprocess.Popen("cd " + detector_path + " && cat NODE_*/output8.0/query_* > result.pairs",
                                     shell=True,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
    export_script.wait()


if __name__ == "__main__":
    clone_detector_path = "/media/viewv/Data/SourcererCC/clone-detector"
    tokenizer_path = "/media/viewv/Data/SourcererCC/tokenizers/file-level"
    jupyter_so_path = "/media/viewv/Data/jupyter_so/"
    db = DataBase()
    # zip_path = "/media/viewv/Data/jupyter_so/jupyter_zip"
    # write_jupyter_code_into_zip(zip_path)
    # zip_path = "/media/viewv/Data/jupyter_so/so_zip"
    # write_so_code_into_zip(zip_path)
    # db.mysql.commit()

    # gen_projects_list(jupyter_so_path, jupyter_so_path)
    # cleanup(tokenizer_path)
    # gen_token(tokenizer_path)
    # gen_query_file(tokenizer_path, 2)
    cp_query_file(tokenizer_path, 2)
    cp_blocks_file(tokenizer_path)
    # run_controller(clone_detector_path)
    # export_result(clone_detector_path)
