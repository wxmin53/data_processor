import pandas as pd
import mysql.connector


# 分块处理数据
def process_data_chunk(data_chunk, column_name):
    data_chunk[column_name] = data_chunk[column_name].str.lower()
    return data_chunk


# 保存数据到文件
def save_to_file(data, file_path, file_format):
    if file_format == 'xlsx':
        data.to_excel(file_path, index=False)
    elif file_format == 'json':
        data.to_json(file_path, orient='records')


# 保存数据到数据库
def save_to_db(data, host, user, password, database, table):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()

    for _, row in data.iterrows():
        values = tuple(row)
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table} VALUES ({placeholders})"
        cursor.execute(query, values)

    connection.commit()
    cursor.close()
    connection.close()

# 从XLSX文件分块提取数据
def extract_data_from_xlsx(file_path, chunk_size=10000):
    chunks = pd.read_excel(file_path, chunksize=chunk_size)
    for chunk in chunks:
        yield chunk

# 从MySQL数据库分块提取数据
def extract_data_from_mysql(host, user, password, database, query, chunk_size=10000):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()
    cursor.execute(query)

    while True:
        chunk = cursor.fetchmany(chunk_size)
        if not chunk:
            break
        yield pd.DataFrame(chunk, columns=cursor.column_names)

    cursor.close()
    connection.close()

# 主函数
def main():
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


if __name__ == "__main__":
    main()
