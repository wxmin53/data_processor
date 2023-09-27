#!/usr/bin/python
import copy
import os
import csv
import json
import pandas as pd

"""
需求：从阿里云平台获取标准的问答库，完成清洗和处理，生成用于自研 FAQ 的数据
step 1：清洗阿里云平台导出原始数据的答案
step 2：拆分相似问，输出文件完整版数据_拆分后.json 注意：pandas 读取 excel 后的 NaN 要替换为""
step 3：提取相似问题拆分后json文件的问答库里的问题和答案，分别保存为问题的 new_all_corpus.csv 文件和问答对的 new_all_qa_pair.csv 文件
todo：添加到data_processor项目中，完成全流程自动化
"""

base_dir = os.getcwd()


class Data_Processor:
    def __init__(self):
        self.new_all_corpus = list()
        self.new_all_qa_pair = list()
        self.ori_path = "/Users/wxm/work/datasets/clean_data/完整版数据_拆分后.json"
        self.new_all_qa_pair_file = os.path.join(base_dir, "new_all_qa_pair.csv")
        self.new_all_corpus_file = os.path.join(base_dir, "new_all_corpus.csv")
        self.ori_data = self.read_json(self.ori_path)

    def read_json(self, path):
        with open(path, "r", encoding="utf-8") as reader:
            return json.loads(reader.read())

    def write_csv(self, csv_file, data_list):
        with open(csv_file, mode='w+', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            for row in data_list:
                writer.writerow(row)

    def get_data(self):
        for line in self.ori_data:
            ques = line["question"]
            ans = line["answer"]
            self.new_all_corpus.append([ques])
            self.new_all_qa_pair.append([ques + '\t' + ans])

    def __call__(self):
        self.get_data()
        self.write_csv(self.new_all_corpus_file, self.new_all_corpus)
        self.write_csv(self.new_all_qa_pair_file, self.new_all_qa_pair)


class A:
    def __init__(self):
        self.ori_data_path = "/Users/wxm/work/datasets/clean_data/杭州库0908.xlsx"
        self.store_path = "/Users/wxm/work/datasets/clean_data/完整版数据_拆分后.json"
        self.excel_data = self.read_excel()

    def read_excel(self):
        excel_data = pd.read_excel(self.ori_data_path)
        excel_data = excel_data.fillna('', inplace=False)
        excel_data = excel_data.to_dict(orient='records')
        return excel_data

    def strip_question(self):
        new_data = []
        quchong_dict = {}
        i = 0
        for line in self.excel_data:
            guanlian_question = []
            i += 1
            if str(line["关联问题"]) != "nan":
                for glq in line["关联问题"].split("\n"):
                    guanlian_question.append(glq)
                line["关联问题"] = guanlian_question
            tmp_dict = copy.deepcopy(line)
            tmp_dict["question"] = line["知识标题"]
            tmp_dict["answer"] = line["答案（默认)【富文本】"].replace(" ", "")
            if str(tmp_dict) not in quchong_dict:
                quchong_dict[str(tmp_dict)] = {}
                new_data.append(tmp_dict)
            if str(line["相似问法"]) == "nan":
                continue

            for qus in line["相似问法"].split("\n"):
                tmp_dict = copy.deepcopy(line)
                i += 1
                tmp_dict["question"] = qus.strip("\n")
                tmp_dict["answer"] = line["答案（默认)【富文本】"].replace(" ", "")
                if str(tmp_dict) not in quchong_dict:
                    new_data.append(tmp_dict)
                    quchong_dict[str(tmp_dict)] = {}
        print(i, len(new_data))
        return new_data

    def write2json(self, data):
        with open(self.store_path, 'w', encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    a = A()
    new_data = a.strip_question()
    a.write2json(new_data)
    # data_processor = Data_Processor()
    # data_processor()
