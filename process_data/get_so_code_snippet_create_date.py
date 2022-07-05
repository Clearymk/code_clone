import json
import requests
import fake_headers
from util.proxy import init
from bs4 import BeautifulSoup


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


def get_code_create_date(post_id, target_code):
    header = fake_headers.Headers().generate()
    url = "https://stackoverflow.com/posts/{}/revisions"
    response = requests.get(url.format(post_id), header)
    bs = BeautifulSoup(response.text, 'html.parser')

    target_code = target_code.strip()
    target_code_create_time = None
    matched = False

    for revision in reversed(bs.find_all("div", attrs={"class": "mb12 js-revision"})):
        if matched:
            break

        create_time = revision.find("span", attrs={"class": "relativetime"}).text
        for code in revision.find_all("code"):
            if code.text.strip() == target_code:
                target_code_create_time = create_time
                matched = True
                break

    return target_code_create_time


if __name__ == "__main__":
    init()
    get_post_vote(40146128)
#     print(get_code_create_date(46908, '''Map<String, String> map = ...
# for (Map.Entry<String, String> entry : map.entrySet())
# {
#     System.out.println(entry.getKey() + "/" + entry.getValue());
# }
# '''))
