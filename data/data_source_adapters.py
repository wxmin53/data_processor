import os
import pandas as pd
import pymysql.cursors
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
    def __init__(self, par_file=None):
        self.par_file = par_file
        if not par_file:
            self.par_file = ""  # todo 读本地文件

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
    def __init__(self, config):
        try:
            self.connection = pymysql.connect(host=config["host"],
                                              user=config["user"],
                                              port=3306,
                                              password=config["password"],
                                              db=config["database"],
                                              charset='utf8',
                                              cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.connection.cursor()
            print("Database connection successful")
        except pymysql.Error as e:
            print("Database connection error:", str(e))

    def execute_query(self, query):
        print(111)
        self.cursor.execute(query)
        try:
            data = self.cursor.fetchall()  # chunk_size
            for chunk in data:
                if not chunk:
                    break
                yield chunk
        except:
            print("sql取数失败")

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
    # main()

    config = {'config': {'local_sql': {}}}
    config['config']['local_sql']['host'] = '192.168.0.10'
    config['config']['local_sql']['port'] = 3306
    config['config']['local_sql']['user'] = 'root'
    config['config']['local_sql']['password'] = 'MdN3mP_w'
    config['config']['local_sql']['database'] = 'mk_faq'
    da = DatabaseAdapter(config['config']['local_sql'])
    sql = 'SELECT question_uuid, question FROM faq_pair WHERE customer_id = 1170  AND status=1'

    for d in da.execute_query(sql):
        print(d)

