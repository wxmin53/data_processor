import re
from data.data_process.sentence_modifier import *
from data.data_process.back_translation.back_translate import *
from data.data_process.gpt_generate import GptRequest

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

# 读数据，通过yield 传递问句
ca = CharacterAugment()



def generate_data(batch, prompt):
    # prompt 数据填充，请求 gpt
    gr = GptRequest()
    gpt_res = gr.request_gpt(prompt.format("原句-" + "\n原句-".join(batch)))
    if gpt_res:
        questions = handle_gpt_res(gpt_res)
        batch.extend(questions)
    return batch


def handle_gpt_res(gpt_res):
    # test_str = """
    # 根据您的要求，我尽量增加了编辑距离，同时保证了语义的一致性和核心词的不变。下面是增强后的数据：
    #
    # json
    # Copy code
    # {
    #   "提示可以缴税后，如何操作？": ["缴税的提示出现后，我应该怎么办？", "提示说缴税可以了，下一步应该怎么操作?", "当系统提示缴税可行后，应如何进一步进行？", "提示缴税可行后，有何操作步骤？"],
    #   "更正登记需要哪些材料": ["更正登记流程需要准备哪些文档?", "进行更正登记时，哪些文件是必要的?", "要更正登记，需提交哪些必要资料?", "更正登记，哪些文件资料是必须的？"],
    #   "不动产权籍调查办理时间": ["办理不动产权籍调查大概需要多长时间？", "不动产权籍调查的处理周期通常是多久？", "进行不动产权籍调查一般要多少时间？", "不动产权籍调查的全程办理时间是？"]
    # }
    # 这些增强后的句子尽量在保持原句意义不变的情况下，通过删减、替换、扩充等手段增加了编辑距离。希望这符合您的需求。
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


def data_augmentation(question, keywords):
    augment_question = [question]
    # 数据回译
    translate_questions = back_translate("萧山房产去哪里办理？", question, keywords)
    augment_question.extend(translate_questions)
    for qus in translate_questions:
        # 字符增减
        if len(qus) > 1:
            charater_question = ca.delete_word(qus, keywords)
            augment_question.extend("".join(charater_question))
    return list(set(augment_question))


def get_faq_synonym_question(data, conf_info):
    prompt = conf_info["config"]["Gpt"]["faq_synonym_prompt"]
    batch_size = conf_info["config"]["Gpt"]["faq_synonym_prompt_limit"]
    keywords = conf_info["keywords"]
    batch = []
    new_data = []
    for line in data:
        augment_question = data_augmentation(line["question"], keywords)
        for idx, question in enumerate(augment_question):
            batch.extend(question)
            if (len("".join(batch)) + len(augment_question[idx+1]) >= batch_size and len(augment_question) > idx+1) \
                    or idx ==len(augment_question)-1:
                gpt_batch = generate_data(batch, prompt)
                batch = []
                new_data.extend([{"synonym_question": q, **line} for q in gpt_batch if q != line["question"]])
    return new_data
