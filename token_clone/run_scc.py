import os
import subprocess


# 将文件地址写入到projects-list
def gen_projects_list(project_path):
    zip_paths = []
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [os.path.join(root, d) for d in dirs]
        files = [fi for fi in files if fi.endswith(".zip")]
        files = [os.path.abspath(os.path.join(root, f)) for f in files]
        if len(files) > 0:
            zip_paths.extend(files)

    with open(os.path.join(project_path, "projects-list.txt"), "w", encoding="utf8") as f:
        for zip_path in zip_paths:
            f.write(zip_path + "\n")


# 清除之前运行是留下的历史数据
def cleanup(clean_up_path):
    cleanup_script = subprocess.Popen(os.path.join(clean_up_path, "cleanup.sh"), shell=True, stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(cleanup_script.communicate())
    print(cleanup_script.returncode)


# 生成token
def gen_token(tokenizer_path):
    tokenizer_script = subprocess.Popen("python " + os.path.join(tokenizer_path, "tokenizer.py"), shell=True,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(tokenizer_script.communicate())
    print(tokenizer_script.returncode) \
        # 将生成的token汇总到blocks.file
    export_blocks = subprocess.Popen("cat "
                                     + os.path.join(tokenizer_path, "files_tokens/*")
                                     + " > "
                                     + os.path.join(tokenizer_path, "blocks.file"),
                                     shell=True,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    export_blocks.wait()


# 生成query_file
def gen_query_file(blocks_path, size):
    tokens = []
    with open(os.path.join(blocks_path, "blocks.file"), "r", encoding="utf8") as f:
        for line in f.readlines():
            tokens.append(line)
    k, m = divmod(len(tokens), size)
    count = 1
    for query_file in (tokens[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(size)):
        with open(os.path.join(blocks_path, "query_{}.file".format(count)), "w", encoding="utf8") as f:
            for token in query_file:
                f.write(token + "\n")
        count += 1


# 复制query_file到clone-detector中
def cp_query_file(query_file_path, size):
    for i in range(0, size):
        cp_script = subprocess.Popen("cp "
                                     + os.path.join(query_file_path, "query_{}.file".format(i + 1))
                                     + " ../../clone-detector/",
                                     shell=True,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        cp_script.wait()


# 复制blocks.file到dataset中
def cp_blocks_file(block_file_path):
    cp_script = subprocess.Popen("cp "
                                 + os.path.join(block_file_path, "blocks.file")
                                 + " ../../clone-detector/input/dataset/",
                                 shell=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
    cp_script.wait()

# 运行查重工具
def run_controller(controller_path):
    cp_script = subprocess.Popen("python " + os.path.join(controller_path, "controller.py"),
                                 shell=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
    cp_script.wait()

# 导出查重结果
def export_result(detector_path):
    export_script = subprocess.Popen("python " + os.path.join(detector_path, "/NODE_*/output8.0/query_*") + " > "
                                     + os.path.join(detector_path, "result.pairs"),
                                     shell=True,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
    export_script.wait()


if __name__ == "__main__":
    clone_detector_path = "/home/viewv/Downloads/SourcererCC/clone-detector"
    tokenizer_path = "/home/viewv/Downloads/SourcererCC/tokenizers"

    gen_projects_list(tokenizer_path)
    cleanup(tokenizer_path)
    gen_token(tokenizer_path)
    gen_query_file(tokenizer_path, 2)
    cp_query_file(tokenizer_path, 2)
    cp_blocks_file(tokenizer_path)
    run_controller(clone_detector_path)
    export_result(clone_detector_path)