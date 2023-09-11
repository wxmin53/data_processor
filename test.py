import pandas as pd
from data.data_source_adapters import FileAdapter
from data.data_store_adapters import StoreAdapter
from data.data_clean.data_cleaning_pipeline import DataCleaner

"""
从文件中读取数据后，圈出待清洗和处理的数据
输入pandas.core.series.Series，处理后的数据也用yield？
"""

par_file = "/Users/wxm/work/datasets/origin_data/杭州库0908.xlsx"
store_path = "/Users/wxm/work/datasets/clean_data"
storage_type = "xlsx"
columns_to_check = ["答案（默认)【富文本】"]

sa = StoreAdapter(store_path)

dc = DataCleaner(lowercase=True,
                 remove_html=True,
                 remove_newlines=True,
                 remove_spcl_char=False,
                 remove_spaces=True,
                 deduplication=True)

# 数据读取和清洗 todo columns_to_check为空时，需要对所有列进行处理
processed_data = pd.DataFrame([dc.normalize_data(data, columns_to_check) for data in FileAdapter(par_file)])
processed_data = dc.data_deduplicate(processed_data, columns_to_check)  # 对输入的列columns_to_check去重

# 数据处理

# 数据存储
sa.store_data(processed_data, storage_type, None)
print(type(processed_data))


def main():
    pass
    input_file = 'input_data.json'
    output_file = 'output_data.json'
    field_name = '待处理字段'


if __name__ == "__main__":
    main()
