import os
import json
import shutil

from util.database import DataBase

# 第一步创建文件夹
if os.path.exists("pylint_check"):
    shutil.rmtree("pylint_check")

os.mkdir("pylint_check")
db = DataBase()


def check_jupyter_code_snippet_exist(jupyter_code_snippet_id):
    count = db.query_by_sql("select count(*) "
                            "from pylint_violation "
                            "where jupyter_id = {}".format(jupyter_code_snippet_id))[0][0]
    if count > 0:
        return True
    return False


def check_so_code_snippet_exist(so_code_snippet_id):
    count = db.query_by_sql("select count(*) "
                            "from pylint_violation "
                            "where so_id = {}".format(so_code_snippet_id))[0][0]
    if count > 0:
        return True
    return False


def detect_jupyter_code_bandit():
    # 第二步导出代码片段到文件当中
    for jupyter_code_snippet_id, code in db.query_by_sql("select id, code "
                                                         "from jupyter.jupyter_code_snippet "
                                                         "where id in "
                                                         "(select jupyter_code_snippet_id "
                                                         "from jupyter.clone_pair "
                                                         "where direction = 1 and clone_type = 1) limit 5"):

        if check_jupyter_code_snippet_exist(jupyter_code_snippet_id):
            continue

        with open("pylint_check/{}.py".format(jupyter_code_snippet_id), "w", encoding="utf8") as f:
            f.writelines(code)

        # 第三步运行bandit得到输出
        os.system(r"pylint --rcfile=./pylint_config.file "
                  "-f json --output pylint_check/report.json  pylint_check/{}.py".format(jupyter_code_snippet_id))

        # 第四步解析输出
        result_json = open("pylint_check/report.json")
        result_json = json.load(result_json)

        for result in result_json:
            print("find violation")
            violation_type = result['type']
            symbol = result['symbol']
            message_id = result['message-id']
            message = result['message']
            db.insert_pylint_violation_jupyter((jupyter_code_snippet_id, violation_type, message_id, message, symbol))

        # 第五步删除文件
        shutil.rmtree("pylint_check")
        os.mkdir("pylint_check")
        print("------------")
    db.mysql.commit()


def detect_so_code_bandit():
    # 第二步导出代码片段到文件当中
    for so_code_snippet_id, code in db.query_by_sql("select id, code "
                                                    "from jupyter.so_code_snippet "
                                                    "where id in "
                                                    "(select so_code_snippet_id "
                                                    "from jupyter.clone_pair "
                                                    "where direction = 1 and clone_type = 2) limit 5"):

        if check_so_code_snippet_exist(so_code_snippet_id):
            continue

        with open("pylint_check/{}.py".format(so_code_snippet_id), "w", encoding="utf8") as f:
            f.writelines(code)

        # 第三步运行bandit得到输出
        os.system(r"pylint --rcfile=./pylint_config.file "
                  "-f json --output pylint_check/report.json  pylint_check/{}.py".format(so_code_snippet_id))

        # 第四步解析输出
        result_json = open("pylint_check/report.json")
        result_json = json.load(result_json)

        for result in result_json:
            print("find violation")
            violation_type = result['type']
            symbol = result['symbol']
            message_id = result['message-id']
            message = result['message']
            db.insert_pylint_violation_so((so_code_snippet_id, violation_type, message_id, message, symbol))

        # 第五步删除文件
        shutil.rmtree("pylint_check")
        os.mkdir("pylint_check")
        print("------------")
    db.mysql.commit()


if __name__ == "__main__":
    # detect_jupyter_code_bandit()
    detect_so_code_bandit()
