from util.database import DataBase
from util.write_log import write_log
from get_so_code_snippet_create_date import get_code_create_date, get_post_vote
from bs4 import BeautifulSoup
from util.proxy import init_proxy


def is_contain_match_code(body, target_code):
    bs = BeautifulSoup(body, 'lxml')
    target_code = target_code.strip()
    for code in bs.find_all("code"):
        if code.text.strip() == target_code:
            return True
    return False


if __name__ == "__main__":
    init_proxy()
    clone_db = DataBase()
    so_db = DataBase("apks")

    for so_code_snippet_id in clone_db.query_by_sql("select distinct so_code_snippet_id "
                                                    "from clone_pair "
                                                    "where clone_pair.so_code_snippet_id > 1863 "
                                                    "order by so_code_snippet_id;"):
        so_code_snippet_id = so_code_snippet_id[0]
        code, so_post_id = clone_db.query_by_sql("select code, so_post_id "
                                                 "from so_code_snippet "
                                                 "where id = {};".format(so_code_snippet_id))[0]
        question_id, question_body = so_db.query_by_sql("select id, body "
                                                        "from apks.question "
                                                        "where id = {}".format(so_post_id))[0]
        target_id = None
        is_question = True

        if is_contain_match_code(question_body, code):
            target_id = question_id
        else:
            is_question = False
            for answer_info in so_db.query_by_sql("select id, body "
                                                  "from apks.answer "
                                                  "where question_id = {}".format(so_post_id)):
                if not target_id:
                    answer_id, answer_body = answer_info
                    if is_contain_match_code(answer_body, code):
                        target_id = answer_id
                else:
                    break

        if target_id:
            create_date = get_code_create_date(target_id, code)
            if is_question:
                vote = get_post_vote(target_id)
            else:
                vote = get_post_vote(question_id, target_id)

            clone_db.insert_clone_so_snippet_info(vote, create_date, so_code_snippet_id)
        else:
            write_log(so_code_snippet_id, "so_log.txt")
