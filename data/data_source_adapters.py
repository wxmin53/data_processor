import os
import pandas as pd
# import xlrd
import mysql.connector
from elasticsearch import Elasticsearch


class loadFolders(object):   # 迭代器
    def __init__(self, par_path):
        self.par_path = par_path

    def __iter__(self):
        for file in os.listdir(self.par_path):
            file_abspath = os.path.join(self.par_path, file)
            if os.path.isdir(file_abspath):  # if file is a folder
                yield file_abspath


class FileAdapter(object):
    def __init__(self, par_file):
        self.par_file = par_file

    def __iter__(self):
        # folders = loadFolders(self.par_path)
        # for folder in folders:              # level directory
        file = self.par_file
        catg = file.split(os.sep)[-1]
        # for file in os.listdir(folder):     # secondary directory
        #     file_path = os.path.join(folder, file)
        if os.path.isfile(file):
            chunks = None
            if "xlsx" in catg:
                chunks = pd.read_excel(file)
            elif "json" in catg:
                chunks = pd.read_json(file)
            elif "csv" in catg:
                chunks = pd.read_csv(file)
            if chunks is not None:
                for index, row in chunks.iterrows():
                    yield row
            # elif "txt" in catg:
            #     this_file = open(file, 'rb')  # rb读取方式更快
            #     content = this_file.read().decode('utf8')
            #     yield content
            #     this_file.close()
        else:  # todo 如果输入为非文件，怎么处理？
            pass


class DatabaseAdapter:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        # for row in self.cursor:
        #     yield row
        while True:
            chunk = self.cursor.fetchmany()  # chunk_size
            if not chunk:
                break
            yield pd.DataFrame(chunk, columns=self.cursor.column_names)

    def close(self):
        self.cursor.close()
        self.connection.close()


class ElasticsearchAdapter:
    def __init__(self, host, port):
        self.client = Elasticsearch([{'host': host, 'port': port}])

    def execute_query(self, index, query):
        result = self.client.search(index=index, body=query)
        for hit in result['hits']['hits']:
            yield hit['_source']

    def close(self):
        self.client.close()


def main():
    current_directory = os.getcwd()
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))

    # 使用文件适配器
    # file_path = os.path.join(parent_directory, 'tests/origin_data/杭州库0824.xlsx')
    file_path = '/Users/wxm/work/datasets/clean_data/杭州库0824_添加question和answer拆分相似问句.json'
    file_adapter = FileAdapter(file_path)
    for data in file_adapter:
        print(type(data))

    # 使用数据库适配器
    db_adapter = DatabaseAdapter('localhost', 'user', 'password', 'mydb')

    # 查询大量数据
    query = "SELECT * FROM mytable"
    for row in db_adapter.execute_query(query):
        # 处理每一行数据
        pass

    db_adapter.close()

    # 使用Elasticsearch适配器
    es_adapter = ElasticsearchAdapter('localhost', 9200)

    # 查询大量数据
    index = 'myindex'
    query = {
        "query": {
            "match_all": {}
        }
    }
    for data in es_adapter.execute_query(index, query):
        # 处理每一条数据
        pass

    es_adapter.close()


if __name__ == '__main__':
    main()
