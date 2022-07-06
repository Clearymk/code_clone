import json
import requests
import fake_headers
from util.proxy import init_proxy
from datetime import datetime
from stackapi import StackAPI
from bs4 import BeautifulSoup
from util.code_trimmer import CodeTrimmer


def get_post_vote(question_id, answer_id=0):
    header = fake_headers.Headers().generate()
    score = 0
    if answer_id == 0:
        url = "https://api.stackexchange.com/2.3/posts/{}?site=stackoverflow"
        response = requests.get(url.format(question_id), header)
        response = json.loads(response.content)
        score = response['items'][0]['score']
    else:
        url = "https://api.stackexchange.com/2.3/questions/{}/answers?site=stackoverflow".format(question_id)
        response = requests.get(url.format(question_id), header)
        response = json.loads(response.content)
        for answer in response['items']:
            if answer['answer_id'] == answer_id:
                score = response['items'][0]['score']
                break
    return score


def get_reversion():
    defaultWrapper = '.backoff;.error_id;.error_message;.error_name;.has_more;.items;.quota_max;.quota_remaining;'
    includes = 'revision.body'

    SITE = StackAPI('stackoverflow')
    # See https://stackapi.readthedocs.io/en/latest/user/advanced.html#end-points-that-don-t-accept-site-parameter
    SITE._api_key = None
    data = SITE.fetch('filters/create', base='none', include=defaultWrapper + includes)
    print(data['items'][0]['filter'])


def get_code_create_date(post_id, target_code):
    header = fake_headers.Headers().generate()
    url = "https://api.stackexchange.com/2.3/posts/{}/revisions?site=stackoverflow&filter=!nKzQUQx*Kx"

    response = requests.get(url.format(post_id), header)
    response = json.loads(response.content)

    create_time = None
    matched = False

    for revision in response['items']:
        revision_body = revision['body']
        bs = BeautifulSoup(revision_body, "lxml")
        for code in bs.find_all("code"):
            if matched:
                break
            if CodeTrimmer(code.text).remove_white_spaces() == target_code:
                matched = True
                create_time = datetime.fromtimestamp(revision['creation_date'])
    return create_time


if __name__ == "__main__":
    init_proxy()
    # get_reversion()
    target_code = ""
    print(get_code_create_date(49566213, CodeTrimmer(target_code).remove_white_spaces()))
    # get_post_vote(49566213)
#     print(get_code_create_date(46908, '''Map<String, String> map = ...
# for (Map.Entry<String, String> entry : map.entrySet())
# {
#     System.out.println(entry.getKey() + "/" + entry.getValue());
# }
# '''))
