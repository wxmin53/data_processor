import jieba
import re
from collections import Counter

stop_words = {"办理": "", "需要": "", "可以": "", "资料": "", "什么": "",
             "材料": "", "查询": "", "怎么": "", "预约": "", "哪些": "",
             "哪里": "", "如何": "", "多少": "", "房子": "", "电话": "",
             "杭州": "", "名字": "", "下载": "", "买卖": "", "房屋": "",
             "进度": "", "怎么办": "", "是否": "", "请问": "", "时间": "",
             "周末": "", "证明": "", "买房": "", "上班": "", "几点": "",
             "你好": "", "信息": "", "业务": "", "流程": "", "取消": "",
             "企业": "", "多久": "", "申请": "", "子女": "", "手续": "",
             "个人": "", "网上": "", "交易": "", "不能": "", "提供": "",
             "首次": "", "现在": "", "网点": "", "咨询电话": "", "怎样": "",
             "丢失": ""}
cut_words = ""
for line in open('/Users/wxm/work/datasets/clean_data/用户咨询数据-user_data.txt', encoding='utf-8'):
    line.strip('\n')
    line = re.sub("[A-Za-z0-9\：\·\—\，\。\“ \”]", "", line)
    seg_list = jieba.cut(line, cut_all=False)
    cut_words += (" ".join(seg_list))
all_words = cut_words.split()
# print(all_words)
c = Counter()
for x in all_words:
    if len(x) > 1 and x != '\r\n':
        c[x] += 1

print('\n词频统计结果：')
for (k, v) in c.most_common(200):  # 输出词频最高的前两个词
    if k in stop_words:
        continue
    print("%s:%d" % (k, v))

