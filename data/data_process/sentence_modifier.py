# 随机增删模块
import jieba
import random


class CharacterAugment():
    # 定义插入函数
    def insert_word(self, question, word_to_insert):
        word_list = list(jieba.cut(question))
        # 随机选择一个位置插入
        insert_index = random.randint(0, len(word_list))
        word_list.insert(insert_index, word_to_insert)

    # 定义删除函数，忽略关键词
    def delete_word(self, question, keywords):
        keyword_index = []
        word_list = list(jieba.cut(question))
        # 随机选择一个词进行删除
        if word_list:
            if keywords:  # 使用keyword mask
                keywords = list(set(keywords))  # 过滤重复keywords
                hit_keywords = [keyword for keyword in keywords if keyword in word_list]
                for selected_keyword in hit_keywords:
                    keyword_index.append(word_list.index(selected_keyword))
                if len(keyword_index) == len(word_list):
                    return word_list
                delete_index = random.randint(0, len(word_list) - 1)
                while delete_index in keyword_index:
                    delete_index = random.randint(0, len(word_list) - 1)
            delete_index = random.randint(0, len(word_list) - 1)
            del word_list[delete_index]
        return word_list


# if __name__ == "__main__":
#     import os
#
#     project_directory = os.path.abspath(os.path.join(os.getcwd(), "../.."))
#     ca = CharacterAugment()
    # 插入操作示例
    # if len(words) > 1:
    #     da.insert_word(words, "请问")
    #     print("插入后的问题:", "".join(words))

    # 删除操作示例
    # 示例问题
    # question = "如何办理不动产权证？"
    # keywords = [line.strip() for line in open(os.path.join(project_directory, "configure/keywords.txt"), "r")]
    # if len(question) > 1:
    #     word_list = ca.delete_word(question, keywords)
    #     print("删除后的问题:", "".join(word_list))
