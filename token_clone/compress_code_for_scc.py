from util.database import DataBase
from zipfile import ZipFile
import os


def write_jupyter_code_into_zip(jupyter_zip_path):
    # max id 5366231
    for jupyter_path in db.query_jupyter_id_from_jupyter_group_by_jupyter_path():
        temp = 1
        jupyter_snippet_id = []

        try:
            for jupyter_id, code in db.query_id_code_from_jupyter_by_jupyter_path(jupyter_path[0]):
                # 将查询到的代码写入python文件中
                with open(str(temp) + ".py", "w", encoding="utf8") as f:
                    f.write(code)
                jupyter_snippet_id.append(jupyter_id)
                temp += 1
            # 将写入的python文件压缩进一个zip文件中
            # os.path.splitext(jupyter_path[0].split("\\")[-1])[0] 得到文件名
            jupyter_zip_file = writer_into_zip(temp, os.path.splitext(jupyter_path[0].split("\\")[-1])[0],
                                               jupyter_zip_path)

            for i in range(1, temp):
                db.update_zip_path_by_jupyter_id(jupyter_snippet_id[i - 1],
                                                 os.path.join(jupyter_zip_file, str(i) + ".py"))
        except Exception as e:
            print(e)


def write_so_code_into_zip(so_zip_path):
    for so_post_id in db.query_so_id_from_so_group_by_post_id():
        temp = 1
        so_snippet_id = []

        try:
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
        except Exception as e:
            print(e)


def writer_into_zip(file_range, zip_file_name, zip_path):
    if zip_file_name == "":
        print()
    zip_file = zip_path + "/" + zip_file_name + ".zip"

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


if __name__ == "__main__":
    db = DataBase()
    zip_path = "/media/viewv/Data/jupyter_so/jupyter_zip"
    write_jupyter_code_into_zip(zip_path)
    db.mysql.commit()
    # zip_path = "/media/viewv/Data/jupyter_so/so_zip"
    # write_so_code_into_zip(zip_path)
