import os
import openpyxl
import json
import csv
import xlrd
import mysql.connector
import pandas as pd
import mysql.connector
from elasticsearch import Elasticsearch
from utils import get_current_time

cur_time = get_current_time()
file_name = "processed_data" + cur_time


class StoreAdapter(object):
    def __init__(self, store_path):
        self.store_path = store_path

    def store_data(self, processed_data, storage_type, config):
        if storage_type == "xlsx":
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.append(["Cleaned Column 1", "Cleaned Column 2", "Cleaned Column 3"])

            for data in processed_data:
                sheet.append(data)

            workbook.save(os.path.join(self.store_path, file_name + ".xlsx"))
            print("数据已存储为xlsx文件")

        elif storage_type == "json":
            with open(os.path.join(self.store_path, file_name + ".json"), "w") as json_file:
                json.dump(processed_data, json_file, indent=4, ensure_ascii=False)
            print("数据已存储为json文件")

        elif storage_type == "csv":
            with open(os.path.join(self.store_path, file_name + ".csv"), "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                # writer.writerow(["Cleaned Column 1", "Cleaned Column 2", "Cleaned Column 3"])
                for data in processed_data:
                    writer.writerow(data)

            print("数据已存储为csv文件")

        elif storage_type == "txt":
            with open(os.path.join(self.store_path, file_name + ".txt"), "w", encoding="utf-8") as txt_file:
                for data in processed_data:
                    txt_file.write("\t".join(map(str, data)) + "\n")
            print("数据已存储为txt文件")

        elif storage_type == "mysql":
            connection = mysql.connector.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"],
                database=config["database"]
            )

            cursor = connection.cursor()

            for data in processed_data:
                query = "INSERT INTO processed_data (cleaned_column1, cleaned_column2, cleaned_column3) VALUES (%s, %s, %s)"
                cursor.execute(query, data)
                connection.commit()

            connection.close()
            print("数据已存储到MySQL数据库")


def main():
    pass


if __name__ == '__main__':
    main()
