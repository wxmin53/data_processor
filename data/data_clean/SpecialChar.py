import re

"""
Description: 处理文本的特殊符号、空格，将其替换为一个空格 or将其删除？
Prompt: code in Python3 env
"""


# 正则对字符串清洗
def textParse(str_doc):
    # 正则过滤掉特殊符号、标点、英文、数字等。
    r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-./:：;；|<=>?@，—。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    # 去除空格
    r2 = '\s+'
    # 去除换行符
    str_doc = re.sub(r1, ' ', str_doc)
    # 多个空格成1个
    str_doc = re.sub(r2, ' ', str_doc)
    # 去除换行符
    # str_doc = str_doc.replace('\n',' ')
    # 去除制表符
    str_doc = str_doc.replace("\t", "").replace("\x0b", "").replace("\x0c", "")
    return str_doc