import time

from util.database import DataBase
from util.write_log import write_log
from find_matched_so_info import get_code_create_date, get_post_vote
from bs4 import BeautifulSoup
from util.proxy import init_proxy
from util.code_trimmer import CodeTrimmer
import requests

controller = "http://127.0.0.1:2390/proxies/"
proxy_url = controller + "%F0%9F%9A%80%20%E8%8A%82%E7%82%B9%E9%80%89%E6%8B%A9"

proxy_group = [
    '台湾 TW 01', '台湾 TW 02', '台湾 TW 03', '台湾 TW 04', '台湾 TW 05', '台湾 TW 06', '台湾 TW 07', '台湾 TW 08',
    '新加坡 SG 01', '新加坡 SG 02', '新加坡 SG 03', '新加坡 SG 04', '新加坡 SG 05', '新加坡 SG 06', '新加坡 SG 07', '新加坡 SG 08',
    '日本 JP 01', '日本 JP 02', '日本 JP 03', '日本 JP 04', '日本 JP 05', '日本 JP 06', '日本 JP 07', '日本 JP 08',
    '韩国 KR 01', '韩国 KR 02', '韩国 KR 03', '韩国 KR 04', '韩国 KR 05', '韩国 KR 06', '韩国 KR 07', '韩国 KR 08',
    '香港 HK 01', '香港 HK 02', '香港 HK 03', '香港 HK 04', '香港 HK 05', '香港 HK 06', '香港 HK 07', '香港 HK 08', '香港 HK 09',
    '香港 HK 10'
]


def change_proxy(current_cid):
    current_cid = (current_cid + 1) % len(proxy_group)
    proxy_name = proxy_group[current_cid]
    print("Change proxy: " + proxy_name)
    r = requests.put(proxy_url, json={"name": proxy_name})
    print(r.status_code)
    return current_cid


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
    exception_count = 0
    current_cid = -1

    for so_code_snippet_id in clone_db.query_by_sql("select distinct so_code_snippet_id "
                                                    "from clone_pair "
                                                    "where clone_pair.so_code_snippet_id > 821286 "
                                                    "order by so_code_snippet_id;"):
        if exception_count >= 5:
            exception_count = 0
            current_cid = change_proxy(current_cid)

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
            try:
                create_date = get_code_create_date(target_id, CodeTrimmer(code).remove_white_spaces())
                time.sleep(1)
                if is_question:
                    vote, is_accept = get_post_vote(target_id)
                else:
                    vote, is_accept = get_post_vote(question_id, target_id)

                clone_db.insert_clone_so_snippet_info(vote, create_date, so_code_snippet_id)
                time.sleep(1)
            except Exception as e:
                exception_count += 1
                print(e)
                time.sleep(1)
                write_log(so_code_snippet_id, "so_log.txt")
        else:
            write_log(so_code_snippet_id, "so_log.txt")
