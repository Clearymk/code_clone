import os
import re

import pycodestyle
from util.database import DataBase

# 对于Type 1克隆，只需要检测其中的一个代码片段即可；对于Type 2,3克隆需要两个代码片段都需要检测
# 检测流程 1，得到所需的代码片段 2.将其写入文件当中 3.使用pycodestyle进行检测

db = DataBase()
message_re = re.compile(r'^(?P<count>\d+)\s*(?P<rule>\w\d+) (?P<description>.+)')


def check_jupyter_code_snippet_exist(jupyter_code_snippet_id):
    count = db.query_by_sql("select count(*) "
                            "from style_violation "
                            "where jupyter_id = {}".format(jupyter_code_snippet_id))[0][0]
    if count > 0:
        return True
    return False


def check_so_code_snippet_exist(so_code_snippet_id):
    count = db.query_by_sql("select count(*) "
                            "from style_violation "
                            "where so_id = {}".format(so_code_snippet_id))[0][0]
    if count > 0:
        return True
    return False


def detect_jupyter_code_style():
    for jupyter_code_snippet_id, code in db.query_by_sql("select id, code "
                                                         "from jupyter.jupyter_code_snippet "
                                                         "where id in "
                                                         "(select jupyter_code_snippet_id "
                                                         "from jupyter.clone_pair "
                                                         "where direction = 1 and clone_type = 1)"):
        if check_so_code_snippet_exist(jupyter_code_snippet_id):
            continue
        style = pycodestyle.StyleGuide()

        with open("{}.py".format(jupyter_code_snippet_id), "w", encoding="utf8") as f:
            f.writelines(code)

        report = style.check_files(['{}.py'.format(jupyter_code_snippet_id)], )
        stat = report.get_statistics()

        for message in stat:
            for match in message_re.finditer(message):
                count = match.group("count")
                rule = match.group("rule")
                description = match.group("description")
                db.insert_style_violation_jupyter((jupyter_code_snippet_id, rule, description, count))
        os.remove("{}.py".format(jupyter_code_snippet_id))
        print("------------------")
    db.mysql.commit()


def detect_so_code_style():
    for so_code_snippet_id, code in db.query_by_sql("select id, code "
                                                    "from jupyter.so_code_snippet "
                                                    "where id in "
                                                    "(select so_code_snippet_id "
                                                    "from jupyter.clone_pair "
                                                    "where direction = 1 and clone_type = 2)"):
        if check_so_code_snippet_exist(so_code_snippet_id):
            continue
        style = pycodestyle.StyleGuide()

        with open("{}.py".format(so_code_snippet_id), "w", encoding="utf8") as f:
            f.writelines(code)

        report = style.check_files(['{}.py'.format(so_code_snippet_id)], )
        stat = report.get_statistics()

        for message in stat:
            for match in message_re.finditer(message):
                count = match.group("count")
                rule = match.group("rule")
                description = match.group("description")
                db.insert_style_violation_so((so_code_snippet_id, rule, description, count))
        os.remove("{}.py".format(so_code_snippet_id))
        print("------------------")
    db.mysql.commit()


if __name__ == "__main__":
    detect_jupyter_code_style()
    # detect_so_code_style()
