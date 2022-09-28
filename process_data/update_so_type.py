from util.database import DataBase
from bs4 import BeautifulSoup

# 第一步 得到目标代码片段对应的so post id
jupyter_db = DataBase()
apks_db = DataBase("apks")

for code_snippet_info in jupyter_db.query_by_sql("select so_code_snippet.id, so_post_id, code "
                                                 "from clone_so_snippet_info, so_code_snippet "
                                                 "where clone_so_snippet_info.so_id = so_code_snippet.id "
                                                 "and so_code_snippet.id in "
                                                 "(select so_code_snippet_id "
                                                 "from clone_pair "
                                                 "where direction = 1 "
                                                 "and clone_type = 1)"):
    so_id, question_id, code_snippet = code_snippet_info

    # 第二步 得到so post id对应的answer和question的内容
    answers_body = apks_db.query_by_sql("select body "
                                        "from apks.answer "
                                        "where question_id = {} "
                                        "and have_code = 1".format(question_id))

    questions_body = apks_db.query_by_sql("select body "
                                          "from apks.question "
                                          "where id = {} "
                                          "and have_code = 1".format(question_id))
    # 第三步 匹配代码片段和内容 得到代码片段所在是answer还是question（1为question，2为answer）
    so_type = 0

    for question_body in questions_body:
        for code in BeautifulSoup(question_body[0], "lxml").find_all("code"):
            if code.text.__contains__(code_snippet.strip()):
                so_type = 1
                break

    if so_type == 0:
        for answer_body in answers_body:
            for code in BeautifulSoup(answer_body[0], "lxml").find_all("code"):
                if code.text.__contains__(code_snippet.strip()):
                    so_type = 2
                    break

    print(so_type)
    # 第四步update 数据库
    if so_type != 0:
        jupyter_db.update_by_sql("update clone_so_snippet_info set type = {} where so_id = {};".format(so_type, so_id))

jupyter_db.commit()