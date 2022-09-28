from util.database import DataBase
from bs4 import BeautifulSoup
from util.code_trimmer import CodeTrimmer
from get_info_from_stackoverflow import get_code_create_date, get_matched_post_info
from util.write_log import write_log
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def is_contain_match_code(body, target_code):
    bs = BeautifulSoup(body, 'lxml')
    for code in bs.find_all("code"):
        if CodeTrimmer(code.text).remove_white_spaces() == CodeTrimmer(target_code).remove_white_spaces():
            return True
    return False


def init_driver():
    options = webdriver.ChromeOptions()
    prefs = {
        'safebrowsing.enabled': 'false',
        'profile.default_content_setting_values': {
            'images': 2,
            'permissions.default.stylesheet': 2,
            'javascript': 2
        }
    }
    options.add_experimental_option('prefs', prefs)
    return webdriver.Chrome(ChromeDriverManager().install(), options=options)


if __name__ == "__main__":
    clone_db = DataBase()
    # driver = init_driver()
    so_db = DataBase("apks")

    for so_code_snippet_id in clone_db.query_by_sql("select so_id from clone_so_snippet_info where type = 0"):
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
            if is_question:
                clone_db.update_by_sql("update clone_so_snippet_info set type = 1 where so_id = {}".format(so_code_snippet_id))
            else:
                clone_db.update_by_sql("update clone_so_snippet_info set type = 2 where so_id = {}".format(so_code_snippet_id))
        # if target_id:
        #     try:
        #         create_date = get_code_create_date(driver, target_id, CodeTrimmer(code).remove_white_spaces())
        #         if is_question:
        #             vote, is_accept = get_matched_post_info(driver, target_id)
        #         else:
        #             vote, is_accept = get_matched_post_info(driver, question_id, target_id)
        #
        #         clone_db.insert_clone_so_snippet_info(vote, create_date, so_code_snippet_id, is_accept)
        #     except Exception as e:
        #         print(e)
        #         write_log(so_code_snippet_id, "so_log.txt")
    clone_db.commit()
    # driver.quit()
