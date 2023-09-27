import re
import json
from data.data_process.sentence_modifier import *
from data.data_process.back_translation import *
from data.data_process.gpt_generate import request_gpt

"""
去除重复项、噪声、特殊字符和不必要的空格。
步骤2：数据增强
2.1 同义词替换：使用自然语言处理库（如NLTK或spaCy）来查找问题中的同义词，并替换一些词以生成新问题。
2.2 句法变换：使用语法分析工具（如Stanford NLP）来修改句子结构，如改变语法关系、主谓宾等。
2.3 单词插入和删除：随机选择一些单词并进行插入或删除操作，确保生成问题的语法正确性和合理性。
2.4 词性标记替换：替换问题中的词性标记，以改变句子的结构。
2.5 回译：jieba 分词统计词频获得关键词，在回译的过程中关键词
步骤3：生成模型
3.1 使用预训练的文本生成模型（如GPT-3.5或更高版本）来生成与原问题相似的问题。提供一些上下文或问题的变种，以让模型生成更多相似问题。
"""


class SynonymQuestionGenerator():
    def __init__(self):
        self.ca = CharacterAugment()

    def generate_data(self, batch, prompt):
        # prompt数据填充，请求gpt
        result = prompt.format("原句-" + "\n原句-".join(batch))
        gpt_res = request_gpt(result)
        if gpt_res and type(gpt_res) is dict:
            batch.extend(gpt_res)
        # if gpt_res:
        #     questions = self.handle_gpt_res(gpt_res)
        #     batch.extend(questions)
        return batch

    def handle_gpt_res(self, gpt_res):
        # test_str = """
        test_str = {
            "本人如何开具“房产证明”/查册？": [
                "如何申请房产证明？",
                "如何查询房屋产权证？",
                "如何查看自己的不动产权证？",
                "如何办理房屋查册？",
                "如何查询房屋权属证明？",
                "如何开具房产权证明书？"
            ],
            "如何查看及下载缴费票据？": [
                "如何查询物业费缴费票据？",
                "如何下载物业费缴费票据？",
                "如何查看物业管理费缴费记录？",
                "如何查询房屋税费缴费记录？",
                "如何下载房屋税费缴费票据？",
                "如何查看房产税缴费记录？"
            ],
            "如何查询房产证是否办理好了？": [
                "如何查询房产证是否下来？",
                "如何查询房屋产权证是否已经办好？",
                "如何查看房屋产权证的办理进度？",
                "如何查询房产证的办理状态？",
                "如何知道房屋产权证已经制作好了？",
                "如何查询房屋产权证的领取时间？"
            ],
            "婚内夫妻析产或离婚析产流程是怎样？": [
                "夫妻离婚后房产如何处理？",
                "离婚后如何处理房产？",
                "夫妻离婚后房屋怎么分割？",
                "离婚后如何分割共同财产？",
                "夫妻共同财产如何分割？",
                "离婚后财产如何分割？"
            ],
            "去珠海市不动产登记中心及各分中心办事大厅需要预约吗？": [
                "去不动产登记中心需要预约吗？",
                "去珠海不动产登记中心需要预约吗？",
                "去不动产登记分中心需要预约吗？",
                "去珠海不动产登记分中心需要预约吗？",
                "去不动产登记大厅需要预约吗？",
                "去珠海不动产登记大厅需要预约吗？"
            ],
            "二手房转移登记全流程网办流程是怎么样的？": [
                "二手房网上办理流程是怎样的？",
                "二手房网上过户流程是怎样的？",
                "二手房网上转移登记流程是怎样的？",
                "二手房网上办理过户需要什么条件？",
                "二手房网上过户需要准备什么材料？",
                "二手房网上转移登记需要哪些手续？"
            ],
            "如何查询房产是否有抵押查封情况？": [
                "如何查询房屋是否被查封？",
                "如何查询房产是否被抵押？",
                "如何查看房屋是否有抵押？",
                "如何查询房屋是否被查封？",
                "如何查看房产是否被查封？",
                "如何查询房屋是否被强制执行？"
            ],
            "律师查询要带什么资料？": [
                "找律师需要准备哪些资料？",
                "律师查询需要携带哪些资料？",
                "律师咨询需要准备哪些材料？",
                "律师咨询要带什么资料？",
                "律师咨询需要携带哪些证件？",
                "律师查询需要带哪些证件？"
            ],
            "房产证满几年可以上市交易？": [
                "房产证多少年可以上市交易？",
                "房产证几年后可以上市交易？",
                "房产证满多久可以上市交易？",
                "房产证满多少年可以交易？",
                "房产证满几年可以交易？",
                "房产证多久可以上市交易？"
            ]
        }
        # """
        questions = []
        pattern = r'{[^{}]*}'
        # 使用正则表达式找到JSON数据部分
        match = re.search(r'{[^{}]*}', gpt_res)
        if match:
            json_text = match.group()
            # 解析JSON数据为字典
            try:
                data = json.loads(json_text)
            except json.JSONDecodeError as e:
                raise "解析JSON时出错：{e}"
        for key, value in data.items():
            questions.append(key)
            questions.extend(value)
        return questions

    def data_augmentation(self, question, keywords):
        augment_question = [question]
        # 数据回译
        try:
            translate_questions = trans_func(question, keywords)
            augment_question.extend(translate_questions)
        except:
            pass
        for qus in list(set(augment_question)):
            # 字符增减
            if len(qus) > 1:
                charater_question = self.ca.delete_word(qus, keywords)
                augment_question.extend("".join(charater_question))
        return list(set(augment_question))

    def get_faq_synonym_question(self, data, conf_info):
        prompt = conf_info["config"]["gpt"]["faq_synonym_prompt"]
        batch_size = int(conf_info["config"]["gpt"]["faq_synonym_prompt_limit"])
        # keywords = conf_info["keywords"]
        batch = []
        new_data = []
        for idx, line in enumerate(data):
            augment_question = [line["question"]]
            # augment_question = self.data_augmentation(line["知识标题"], keywords)
            for question in augment_question:
                batch.append(question)
                # 限制输入问题的字数：如果prompt提示+问题长度小于限制长度并且不是最后一个问题，则继续遍历
                if len(prompt) + len("原句-".join(batch)) < batch_size and idx != len(data)-1:
                    continue
                gpt_batch = self.generate_data(batch, prompt)
                if line["question"] in gpt_batch: gpt_batch.remove(line["question"])
                new_data.append({"synonym_question": "\n".join(gpt_batch), **line}) # for q in gpt_batch if q != line["知识标题"]])
                # new_data.append({"question": line["知识标题"], "synonym_question": "\n".join(gpt_batch)})
                batch = []
        return new_data


if __name__ == "__main__":
    pass
