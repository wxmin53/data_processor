import re
from html import unescape
from data.data_clean.DealHtml import *
from data.data_clean.SpecialChar import *


class DataCleaner():
    def __init__(self, lowercase=False,
                 remove_html=False,
                 remove_newlines=False,
                 remove_spcl_char=False,
                 remove_spaces=False,
                 deduplication=False):
        self.lowercase = lowercase
        self.remove_html = remove_html
        self.remove_newlines = remove_newlines
        self.remove_spcl_char = remove_spcl_char
        self.remove_spaces = remove_spaces
        self.deduplication = deduplication

    def normalize_data(self, series, columns_to_check):
        for column in columns_to_check:
            text = series[column]
            if text is None or type(text) is not str:
                series[column] = text
                continue

            # 小写化
            if self.lowercase:
                text = text.lower()

            # 删除HTML特殊字符 实体字符&lt;对应的unicode字符为<，实体字符&gt;对应的unicode字符为>
            if self.remove_html:
                text = filter_tags(text)

            # 删除换行符
            if self.remove_newlines:
                text = text.replace('\n', '').replace('\r', '')

            # 删除换行符
            if self.remove_spaces:
                text = text.replace(' ', '')

            # 删除制表符\t、垂直制表符\x0b、换页符\x0c
            if self.remove_spcl_char:
                text = textParse(text)

            series[column] = text

        return series

    def data_deduplicate(self, df, columns_to_check):
        if self.deduplication:
            df.drop_duplicates(subset=columns_to_check)
        data = df.to_dict(orient='records')
        return data
