import pandas as pd
from data.data_cleaning import *
from tool.utils import ReadFile

"""
获取清洗模块配置化选项
lowercase=False,
remove_html=False,
remove_newlines=False,
remove_spcl_char=False
"""

rd = ReadFile()
dc = DataCleaning()
# sheet_name = '可导入版本'
sheet_name = '完整版本'


def get_clean_data(text):
    new_data = []
    for row in text:
        for key, value in row.items():
            if "富文本" not in key:
                continue
            row[key] = dc.data_cleaning(value, lowercase, remove_html, remove_newlines, remove_spcl_char)
        new_data.append(row)
    return new_data


def main():
    file_path = "/Users/wxm/Documents/MK/dirty_data/杭州库0824.xlsx"
    text = rd.read_xlsx_to_dict(file_path, sheet_name)  # 读取XLSX文件并返回字典列表
    target_test = get_field_data_from_dict()  # 从多字段文本中获取待处理的数据

    text = get_clean_data(text)
    df = pd.DataFrame(text)

    # 保存DataFrame到Excel文件
    excel_file_path = sheet_name + 'data'  # 指定保存的文件名
    df.to_csv(excel_file_path + '.csv', index=False, encoding='utf-8')
    df.to_json(excel_file_path + '.json', orient='records', force_ascii=False, lines=True)
    # df.to_excel(excel_file_path, index=False)


    # 设置参数
    source = 'xlsx'  # 'xlsx' 或 'db'，选择数据来源
    save_to = 'xlsx'  # 'xlsx'、'json' 或 'db'，选择保存方式
    column_name = 'Name'  # 选择要小写化处理的列名或字段名

    # XLSX 文件路径
    xlsx_file_path = 'data.xlsx'

    # MySQL 连接信息
    mysql_host = 'localhost'
    mysql_user = 'user'
    mysql_password = 'password'
    mysql_database = 'database'
    mysql_query = 'SELECT * FROM table'

    # 保存文件路径
    save_file_path = 'cleaned_data'
    file_format = 'xlsx'  # 'xlsx' 或 'json'
    save_table = 'cleaned_data_table'

    if source == 'xlsx':
        extractor = extract_data_from_xlsx(xlsx_file_path)
    else:  # 'db'
        extractor = extract_data_from_mysql(mysql_host, mysql_user, mysql_password, mysql_database, mysql_query)

    for data_chunk in extractor:
        processed_data = process_data_chunk(data_chunk, column_name)

        if save_to == 'xlsx' or save_to == 'json':
            save_to_file(processed_data, f'{save_file_path}.{file_format}', file_format)

        if save_to == 'db':
            save_to_db(processed_data, mysql_host, mysql_user, mysql_password, mysql_database, save_table)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
