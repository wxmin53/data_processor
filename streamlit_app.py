import streamlit as st
import pandas as pd
import sqlite3
import os

# 设置页面标题
st.title('Excel 数据导入和导出')

# 创建一个侧边栏，用于上传 Excel 文件
uploaded_file = st.sidebar.file_uploader("上传 Excel 文件", type=["xlsx", "xls"])

# 数据库连接
conn = sqlite3.connect("data.db")
cur = conn.cursor()


if uploaded_file is not None:
    # 上传 Excel 文件并将其读入 DataFrame
    df = pd.read_excel(uploaded_file)

    # 在界面上显示上传的数据
    st.write("上传的数据：")
    st.write(df)

    # 将数据插入到数据库
    df.to_sql("my_data", conn, if_exists="replace", index=False)

    st.success("数据已成功导入到数据库!")

# 在侧边栏添加按钮以执行导出操作
if st.sidebar.button("导出处理后的数据为 Excel"):
    # 从数据库中提取数据
    query = "SELECT * FROM my_data"
    df = pd.read_sql(query, conn)

    # 在这里添加数据处理逻辑，这里只是一个示例，你可以根据需要进行处理

    # 将处理后的数据导出到 Excel 文件
    export_file_path = "data_file/processed_data.xlsx"
    df.to_excel(export_file_path, index=False)
    st.sidebar.success(f"处理后的数据已成功导出为 {export_file_path}")

# 关闭数据库连接
conn.close()

