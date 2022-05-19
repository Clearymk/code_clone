from util.database import DataBase
from util.code_trimmer import CodeTrimmer
from zipfile import ZipFile
import os


def write_jupyter_code_into_zip(jupyter_zip_path):
    for jupyter_path, min_id, max_id in db.query_jupyter_id_from_jupyter_group_by_jupyter_path():
        temp = 1

        for code in db.query_code_from_jupyter_by_id_range(min_id, max_id):
            # 将查询到的代码写入python文件中
            trimmer = CodeTrimmer(code[0])
            trimmer.remove_comments_and_docstrings()
            code = trimmer.code
            with open(str(temp) + ".py", "w", encoding="utf8") as f:
                f.write(code)
            temp += 1
        # 将写入的python文件压缩进一个zip文件中
        writer_into_zip(temp, jupyter_path.split(os.sep)[-1].split(".")[0], jupyter_zip_path)


def write_so_code_into_zip(so_zip_path):
    for so_post_id, min_id, max_id in db.query_so_id_from_so_group_by_post_id():
        temp = 1

        for code in db.query_code_from_so_by_id_range(min_id, max_id):
            # 将查询到的代码写入python文件中
            trimmer = CodeTrimmer(code[0])
            trimmer.remove_comments_and_docstrings()
            code = trimmer.code
            with open(str(temp) + ".py", "w", encoding="utf8") as f:
                f.write(code)
            temp += 1
        # 将写入的python文件压缩进一个zip文件中, 由于文件名以post_id作为名字，所以不需要移除后缀名
        writer_into_zip(temp, so_post_id.split(os.sep)[-2], so_zip_path)


def writer_into_zip(file_range, zip_file_name, zip_path):
    with ZipFile(os.path.join(zip_path, zip_file_name + ".zip"), "w") as zf:
        for i in range(1, file_range):
            zf.write(str(i) + ".py")
            # 删除写入的python文件
            os.remove(str(i) + ".py")


if __name__ == "__main__":
    db = DataBase()
    zip_path = "jupyter_zip"
    write_jupyter_code_into_zip(zip_path)
    zip_path = "so_zip"
    write_so_code_into_zip(zip_path)
