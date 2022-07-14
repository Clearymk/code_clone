from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from util.code_trimmer import CodeTrimmer
from util.proxy import init_proxy


def get_matched_post_info(driver, question_id, answer_id=-1):
    is_accepted = False
    if answer_id == -1:
        driver.get("https://stackoverflow.com/questions/{}".format(question_id))
        question_content = driver.find_element(By.CSS_SELECTOR, "#question")
        vote = question_content.find_element(By.XPATH, "//div[@itemprop=\"upvoteCount\"]").get_attribute("data-value")
    else:
        driver.get("https://stackoverflow.com/questions/{}".format(answer_id))
        answer_content = driver.find_element(By.XPATH, "//div[@data-answerid=\"{}\"]".format(answer_id))
        vote = answer_content.find_element(By.XPATH, ".//div[@itemprop=\"upvoteCount\"]").get_attribute("data-value")

        try:
            answer_content.find_element(By.XPATH,
                                        ".//div[@class=\"js-accepted-answer-indicator flex--item fc-green-500 py6 mtn8\"]")
            is_accepted = True
        except Exception:
            pass

    return vote, is_accepted


def get_code_create_date(driver, post_id, target_code):
    index = 1
    matched_revision = -1
    matched = False

    while True:
        if matched:
            break

        driver.get("https://stackoverflow.com/revisions/{}/".format(post_id) + str(index))

        if driver.title.__contains__("Page not found"):
            break

        for code in driver.find_elements(By.TAG_NAME, "code"):
            print(code.text)
            if CodeTrimmer(code.text).remove_white_spaces() == CodeTrimmer(target_code).remove_white_spaces():
                matched_revision = index
                matched = True
                break
        index += 1

    driver.get("https://stackoverflow.com/posts/{}/revisions".format(post_id))
    for revision in driver.find_elements(By.XPATH, "//div[@class=\"mb12 js-revision\"]"):
        try:
            revision.find_element(By.XPATH, ".//div[@title=\"revision {}\"]".format(matched_revision))
            create_date = revision.find_element(By.XPATH, ".//span[@class=\"relativetime\"]").get_attribute('title')
            return create_date
        except Exception:
            continue


if __name__ == "__main__":
    # init_proxy()
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
    chrome_driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    get_matched_post_info(chrome_driver, 40471, 22253585)
    # get_code_create_date(40878, CodeTrimmer('''HashMap ''').remove_white_spaces())
    chrome_driver.quit()
