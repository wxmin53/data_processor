import time
import random
import requests
import json
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from retry import retry


chrome_options = Options()


@retry(tries=3, delay=1)
def translate(query_string, source, target):
    url = 'https://translate.google.cn/translate_a/single?'
    param = 'client=gtx&sl=%s&tl=%s&dt=t&q=' % (source, target) + query_string
    response = requests.get(url + param)
    result = json.loads(response.text)
    return {
        "source": result[0][0][1],
        "target": result[0][0][0],
    }

    # base_url = 'https://translate.google.com/?hl=%s' % target
    #
    # if browser.current_url != base_url:
    #     browser.get(base_url)
    #
    # submit = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="source"]')))
    # submit.clear()
    # submit.send_keys(input)
    # WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="tlid-translation translation"]')))
    # source = etree.HTML(browser.page_source)
    # result = source.xpath('//span[@class="tlid-translation translation"]//text()')[0]
    # return result


def back_translate(text, lang_list, sleep_mean=1.0, sleep_dev=0.3):
    """
        参数：
        ------
        text: ``str``
            要回译的文本
        lang_list: ``Iterable[str]``
            要回译的语言代码列表。例如要将一句话从中文翻译到英文再翻译回中文，则指定：
            ``lang_list=("zh-CN", "en", "zh-CN"])``
        sleep_mean: ``float``, optional, default=``1.0``
            延迟均值（为了防止ip被封，需要延迟）
        sleep_dev: ``float``, optional, default=``0.3``
            延迟标准差
        """
    assert len(lang_list) >= 2
    current_text = text
    for i in range(0, len(lang_list) - 2, 2):
        time.sleep(max(0.1, random.gauss(sleep_mean, sleep_dev)))
        current_text = translate(current_text, source=lang_list[i], target=lang_list[i+1])
    return current_text


def trans_func(text, keywords):
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
    schema_list = [["zh-CN", "en", "en", "zh-CN"], ["zh-CN", "ja", "zh-CN"], ["zh-CN", "ko", "zh-CN"]]

    back_trans = []
    for lang_list in schema_list:
        if keywords:  # 使用keyword mask
            keywords = list(set(keywords))  # 过滤重复keywords
            hit_keywords = [keyword for keyword in keywords if keyword in text]
            for selected_keyword in hit_keywords:
                text = text.replace(selected_keyword, "UNK")
                back_translate_res = back_translate(text, lang_list)
                if "UNK" in back_translate_res or "unk" in back_translate_res:
                    back_translate_res = back_translate_res.replace("UNK", selected_keyword)
                    back_translate_res = back_translate_res.replace("unk", selected_keyword)
                    back_trans.append(back_translate_res)

    browser.quit()
    return back_trans


if __name__ == '__main__':
    pass
    # trans = translate("你好世界")
    # print(trans.get("source"))
    # print(trans.get("target"))