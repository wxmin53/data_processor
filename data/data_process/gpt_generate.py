# coding:utf-8
#Note: The openai-python library support for Azure OpenAI is in preview.

import openai

openai.api_type = "azure"
openai.api_base = "https://azure-openai-mkios.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = "66c25b86549e4a81802e58420947c4aa"
engine = "mkios-faq-data-clearing-test20230921"


def request_gpt(content):
    response = openai.ChatCompletion.create(
      engine=engine,
      messages=[{"role": "system", "content": "You are an AI assistant that helps people find information."},
                {"role": "user", "content": content}],
      temperature=0.95,
      # max_tokens=800,
      # top_p=0.4,  # 0.95
      timeout=3,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None)
    choices = response.get('choices', [])
    for choice in choices:
        finish_reason = choice.get("finish_reason", '')
        if finish_reason == 'stop':
            answer = choice.get("message", {}).get("content", '')
            # print(index, '-'*50)
            # print(question)
            return answer


# openai
# class GptRequest():
#     def __init__(self):
#         pass
#
#     def request_gpt(self, prompt):
#         # 请求 api
#         openai.api_key = "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"
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             # model="gpt-4",
#             temperature=0,
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt}
#             ]
#         )
#         # print(response)
#         choices = response.get('choices', [])
#         if len(choices) > 0:
#             finish_reason = choices[0].get("finish_reason", '')
#             if finish_reason == 'stop':
#                 answer = choices[0].get("message", {}).get("content", '')
#                 return answer
#         return None


if __name__ == "__main__":
    pass
    # content = "已知:原问和相似问对应的答案完全相同,要求:根据原问生成10个相似问.返回json格式\n>示例\n原问-查档需要什么材料？\n原问-房产证上如何加配偶的名字？\n返回-{{查档需要什么材料？:[我想查询房龄需要什么资料？,如何查自己名下的房屋档案？,个人要打印自己的不动产信息要什么资料？,...],房产证上如何加配偶的名字？:[婚后夫妻加名如何办理,配偶增名办理流程？,婚前有贷款的房子如何在婚后加配偶的名字？,...]}}\n>按照上面的说明和示例进行操作\n原问-产权是同一个人，两套房产可以一起抵押吗？\n返回:"
    # answer = request_gpt(content)
    # print(answer)
