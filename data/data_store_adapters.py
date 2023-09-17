import os
import json
import csv
import uuid
import hashlib
# import mysql.connector
import pandas as pd
# import mysql.connector
import pymysql.cursors
from tool.utils import get_current_time

cur_time = get_current_time()
file_name = "processed_data" + cur_time


class StoreAdapter(object):
    def __init__(self, store_path):
        self.store_path = store_path

    def store_data(self, processed_data, storage_type, config, name):
        if storage_type == "xlsx":
            processed_data = pd.DataFrame(processed_data)
            processed_data.to_excel(os.path.join(self.store_path, name + cur_time + ".xlsx"), index=False)
            # workbook = openpyxl.Workbook()
            # sheet = workbook.active
            # sheet.append(["Cleaned Column 1", "Cleaned Column 2", "Cleaned Column 3"])
            # for data in processed_data:
            #     sheet.append(data)
            # workbook.save(os.path.join(self.store_path, file_name + ".xlsx"))
            print("数据已存储为xlsx文件")

        elif storage_type == "json":
            with open(os.path.join(self.store_path, name + cur_time + ".json"), "w") as json_file:
                json.dump(processed_data, json_file, indent=4, ensure_ascii=False)
            print("数据已存储为json文件")

        elif storage_type == "csv":
            with open(os.path.join(self.store_path, name + cur_time + ".csv"), "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                # writer.writerow(["Cleaned Column 1", "Cleaned Column 2", "Cleaned Column 3"])
                for data in processed_data:
                    writer.writerow(data)

            print("数据已存储为csv文件")

        elif storage_type == "txt":
            with open(os.path.join(self.store_path, name + cur_time + ".txt"), "w", encoding="utf-8") as txt_file:
                for data in processed_data:
                    txt_file.write("\t".join(map(str, data)) + "\n")
            print("数据已存储为txt文件")

        elif storage_type == "mysql":
            # connection = mysql.connector.connect(
            #     host=config["config"]["local_sql"]["host"],
            #     user=config["config"]["local_sql"]["user"],
            #     password=config["config"]["local_sql"]["password"],
            #     database=config["config"]["local_sql"]["database"],
            #     auth_plugin='mysql_native_password'
            # )

            # cursor = connection.cursor()
            xs1 = []
            xs2 = []
            xs3 = []
            cust_ques2uuid = {}
            for data in processed_data:
                question_hash = str(hashlib.sha1(data["知识标题"].encode('utf-8')).hexdigest())
                uuid_str = str(uuid.uuid1())
                if data["customer_id"] not in cust_ques2uuid:
                    cust_ques2uuid[data["customer_id"]] = {}
                cust_ques2uuid[data["customer_id"]][question_hash] = uuid_str

            for data in processed_data:
                question_hash = str(hashlib.sha1(data["知识标题"].encode('utf-8')).hexdigest())
                uuid_str = cust_ques2uuid[data["customer_id"]][question_hash]
                xs1.append([data["customer_id"], uuid_str, data['类目路径（多级类目用/分隔）'], data['知识标题'], data['答案（默认)【富文本】']])
                for synonymy in data["相似问法"].split("\n"):
                    xs2.append([data["customer_id"], uuid_str, synonymy])
                if not data["关联问题"] or str(data["关联问题"]) == "nan":
                    continue

                for relate in data["关联问题"].split("\n"):
                    relate_ques_hash = str(hashlib.sha1(relate.encode('utf-8')).hexdigest())
                    related_uuid = cust_ques2uuid[data["customer_id"]][relate_ques_hash]
                    xs3.append([data["customer_id"], uuid_str, related_uuid])
            faq_pair_insert = '''
                    INSERT INTO faq_pair (customer_id, question_uuid, category_path, question, answer) VALUES  (%s, %s, %s, %s, %s);
                  '''
            faq_synonymy_question_insert = '''
                                INSERT INTO faq_synonymy_question (customer_id, question_uuid, synonym_question) VALUES  (%s, %s, %s);
                              '''
            faq_correlative_questions_insert = '''
                                INSERT INTO faq_correlative_questions (customer_id, question_uuid, correlate_uuid) VALUES  (%s, %s, %s);
                              '''
            execute_sql_many(db_connect(), faq_pair_insert, xs1)
            execute_sql_many(db_connect(), faq_synonymy_question_insert, xs2)
            execute_sql_many(db_connect(), faq_correlative_questions_insert, xs3)
            print("数据已存储到MySQL数据库")

# def save_db2excel():
# #     todo 1.wenti --> question:uuid; uuid:question;
# 2.biao2  uuid:[q1,q2]
# 3.biao3  uuid:[uuid1,uuid2]
# 4.save excel

def db_connect():
    # sql_host = config_map[db].get('sql_host','127.0.0.1')
    # sql_user = config_map[db].get('sql_user','root')
    # sql_port = int(config_map[db].get('sql_port','3306'))
    # sql_pswd = config_map[db].get('sql_pswd','12345678')
    # if sub_db:
    #     sql_db = sub_db
    # else:
    #     sql_db = config_map[db].get('sql_db', 'dashatao')
    # db_connection = pymysql.connect(host=sql_host,
    #                                 user=sql_user,
    #                                 port=sql_port,
    #                                 password=sql_pswd,
    #                                 db=sql_db,
    #                                 charset='utf8',
    #                                 cursorclass=pymysql.cursors.DictCursor)
    db_connection = pymysql.connect(host='127.0.0.1',
                    user='root',
                    port=3306,
                    password='12345678',
                    db='dashatao',
                    charset='utf8',
                    cursorclass=pymysql.cursors.DictCursor)
    return db_connection


def execute_sql_many(db_connection, sql, xs):
    re = -1
    try:
        with db_connection.cursor() as cursor:
            length = 300
            for i in range(0, len(xs), length):
                re = cursor.executemany(sql, xs[i:i+length])
                if re:
                    db_connection.commit()
    finally:
        db_connection.close()
    return re


def main():
    pass


if __name__ == '__main__':
    main()
