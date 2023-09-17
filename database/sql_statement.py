# import mysql.connector
# from tool.utils import DBHandle

# 获取 customer id
# db_h = DBHandle()
# customer_info_sql = "select customer_id, name from customer_management;"
# content = db_h.read_db(customer_info_sql)
# customer2id_dict = {}
# for row in content:
#     customer2id_dict[row[1]] = row[0]

faq_pair_insert = """
INSERT INTO {} (customer_id, category_path, question, answer) VALUES  (%s, %s, %s, %s);
"""

faq_synonymy_question_insert = """

"""

faq_synonymy_question_id = """SELECT id from faq_pair where customer_id={} and question={}"""
