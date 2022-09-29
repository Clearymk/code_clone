import os
import json
import shutil

from util.database import DataBase

# 第一步创建文件夹
if os.path.exists("bandit_check"):
    shutil.rmtree("bandit_check")

os.mkdir("bandit_check")
db = DataBase()


def check_jupyter_code_snippet_exist(jupyter_code_snippet_id):
    count = db.query_by_sql("select count(*) "
                            "from bandit_violation "
                            "where jupyter_id = {}".format(jupyter_code_snippet_id))[0][0]
    if count > 0:
        return True
    return False


def check_so_code_snippet_exist(so_code_snippet_id):
    count = db.query_by_sql("select count(*) "
                            "from bandit_violation "
                            "where so_id = {}".format(so_code_snippet_id))[0][0]
    if count > 0:
        return True
    return False


def level_mapping(level):
    if level == "LOW":
        return 1
    elif level == "MEDIUM":
        return 2
    elif level == "HIGH":
        return 3
    elif level == "UNDEFINED":
        return 4
    else:
        return -1


def detect_jupyter_code_bandit():
    # 第二步导出代码片段到文件当中
    for jupyter_code_snippet_id, code in db.query_by_sql("select id, code "
                                                         "from jupyter.jupyter_code_snippet "
                                                         "where id in "
                                                         "(select jupyter_code_snippet_id "
                                                         "from jupyter.clone_pair "
                                                         "where direction = 1 and clone_type = 1)"):

        if check_jupyter_code_snippet_exist(jupyter_code_snippet_id):
            continue

        with open("bandit_check/{}.py".format(jupyter_code_snippet_id), "w", encoding="utf8") as f:
            f.writelines(code)

        # 第三步运行bandit得到输出
        os.system("bandit -r bandit_check/ -q -f json -o bandit_check/result.json")

        # 第四步解析输出
        result_json = open("bandit_check/result.json")
        result_json = json.load(result_json)

        for result in result_json['results']:
            violation_code = result['code']
            severity = level_mapping(result['issue_severity'])
            confidence = level_mapping(result['issue_confidence'])
            cwe_link = result['issue_cwe']['link']
            issue_text = result['issue_text']
            violation_id = result['test_id']
            print("found issue!", issue_text)
            db.insert_bandit_violation_jupyter((jupyter_code_snippet_id, violation_code, severity,
                                                confidence, issue_text, cwe_link, violation_id))
        # 第五步删除文件
        shutil.rmtree("bandit_check")
        os.mkdir("bandit_check")
        print("------------")
    db.mysql.commit()


def detect_so_code_bandit():
    # 第二步导出代码片段到文件当中
    for so_code_snippet_id, code in db.query_by_sql("select id, code "
                                                    "from jupyter.so_code_snippet "
                                                    "where id in "
                                                    "(select so_code_snippet_id "
                                                    "from jupyter.clone_pair "
                                                    "where direction = 1 and clone_type = 2)"):

        if check_so_code_snippet_exist(so_code_snippet_id):
            continue

        with open("bandit_check/{}.py".format(so_code_snippet_id), "w", encoding="utf8") as f:
            f.writelines(code)

        # 第三步运行bandit得到输出
        os.system("bandit -r bandit_check/ -q -f json -o bandit_check/result.json")

        # 第四步解析输出
        result_json = open("bandit_check/result.json")
        result_json = json.load(result_json)

        for result in result_json['results']:
            violation_code = result['code']
            severity = level_mapping(result['issue_severity'])
            confidence = level_mapping(result['issue_confidence'])
            cwe_link = result['issue_cwe']['link']
            issue_text = result['issue_text']
            violation_id = result['test_id']
            print("found issue!", issue_text)
            db.insert_bandit_violation_jupyter((so_code_snippet_id, violation_code, severity,
                                                confidence, issue_text, cwe_link, violation_id))
        # 第五步删除文件
        shutil.rmtree("bandit_check")
        os.mkdir("bandit_check")
        print("------------")
    db.mysql.commit()


if __name__ == "__main__":
    detect_jupyter_code_bandit()
    # detect_so_code_bandit()
