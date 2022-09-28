from util.database import DataBase
from bs4 import BeautifulSoup


def is_contain_match_code(body, target_code):
    bs = BeautifulSoup(body, 'lxml')
    target_code = target_code.strip()
    for code in bs.find_all("code"):
        if code.text.strip() == target_code:
            return True
    return False


# type 1 为question type 2 为answer
if __name__ == "__main__":
    clone_db = DataBase()

    so_db = DataBase("apks")

    for so_code_snippet_id in clone_db.query_by_sql("select distinct so_code_snippet_id "
                                                    "from clone_pair "
                                                    "where direction = 1 "
                                                    "order by so_code_snippet_id"):
        so_type = 0
        so_code_snippet_id = so_code_snippet_id[0]
        code, so_post_id = clone_db.query_by_sql("select code, so_post_id "
                                                 "from so_code_snippet "
                                                 "where id = {};".format(so_code_snippet_id))[0]
        question_id, question_body = so_db.query_by_sql("select id, body "
                                                        "from apks.question "
                                                        "where id = {}".format(so_post_id))[0]
        is_question = True

        if is_contain_match_code(question_body, code):
            target_id = question_id
        else:
            is_question = False

        if is_question:
            clone_db.update_by_sql("update so_code_snippet set clone_type = 1 "
                                   "where id = {}".format(so_code_snippet_id))
            print("update so code snippet id = {} and so post id = {}, type to question".format(so_code_snippet_id,
                                                                                                so_post_id))
            print(code)
        else:
            clone_db.update_by_sql("update so_code_snippet set clone_type = 2 "
                                   "where id = {}".format(so_code_snippet_id))
            print("update so code snippet id = {} and so post id = {}, type to answer".format(so_code_snippet_id,
                                                                                              so_post_id))
            print(code)
        print("-------")
