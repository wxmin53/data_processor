import streamlit as st
import pandas as pd
import sqlite3


def tab1_fun():
    import streamlit as st
    import pandas as pd
    # 设置页面标题
    st.title('Excel 数据导入和导出')

    # 创建一个侧边栏，用于上传 Excel 文件
    uploaded_file = st.sidebar.file_uploader("上传 Excel 文件", type=["xlsx", "xls"])

    # 数据库连接
    # conn = sqlite3.connect("data.db")
    # cur = conn.cursor()

    if uploaded_file is not None:
        # 上传 Excel 文件并将其读入 DataFrame
        df = pd.read_excel(uploaded_file)

        # 在界面上显示上传的数据
        st.write("上传的数据：")
        st.write(df)

        # # 将数据插入到数据库
        # df.to_sql("my_data", conn, if_exists="replace", index=False)

        st.success("数据已成功导入到数据库!")

    # 在侧边栏添加按钮以执行导出操作
    if st.sidebar.button("导出处理后的数据为 Excel"):
        # 从数据库中提取数据
        query = "SELECT * FROM my_data"
        # df = pd.read_sql(query, conn)

        # 在这里添加数据处理逻辑，这里只是一个示例，你可以根据需要进行处理

        # 将处理后的数据导出到 Excel 文件
        export_file_path = "data_file/processed_data.xlsx"
        df.to_excel(export_file_path, index=False)
        st.sidebar.success(f"处理后的数据已成功导出为 {export_file_path}")

    # 关闭数据库连接
    # conn.close()

    import streamlit as st
    import pandas as pd
    import sqlite3
    import re
    from bs4 import BeautifulSoup

    # Streamlit 页面标题
    st.title("数据处理和标注应用")

    # 选择文件清洗选项
    st.sidebar.header("文件清洗选项")
    to_lower = st.sidebar.checkbox("将文本转换为小写")
    remove_html = st.sidebar.checkbox("去除 HTML 标签")
    remove_special_chars = st.sidebar.checkbox("删除特殊字符")

    # 文件上传
    uploaded_file = st.file_uploader("上传文件", type=["txt", "csv", "xlsx"])

    if uploaded_file:
        # 读取上传的文件
        if uploaded_file.type == "text/plain":
            df = pd.read_csv(uploaded_file, delimiter="\t")  # 适应不同的文件类型
        elif uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(uploaded_file)

        # 文件清洗
        if to_lower:
            df['text'] = df['text'].str.lower()

        if remove_html:
            df['text'] = df['text'].apply(lambda x: BeautifulSoup(x, "html.parser").get_text())

        if remove_special_chars:
            df['text'] = df['text'].apply(lambda x: re.sub(r'[^\w\s]', '', x))

        # 数据库连接
        # conn = sqlite3.connect('your_database.db')

        # 数据导入到数据库
        # df.to_sql('data', conn, if_exists='replace', index=False)

        # 数据导出为文件
        export_format = st.selectbox("选择导出格式", ["CSV", "Excel"])
        if export_format == "CSV":
            st.write("导出为CSV文件")
            st.download_button("点击下载", df.to_csv(index=False), key='download_csv')
        elif export_format == "Excel":
            st.write("导出为Excel文件")
            st.download_button("点击下载", df.to_excel(index=False), key='download_excel')

        # 关闭数据库连接
        # conn.close()

    # 数据库操作
    st.header("数据库操作")

    # 连接数据库
    # conn = sqlite3.connect('your_database.db')

    # 查询数据库中的数据
    # query = "SELECT * FROM data"
    # df_from_db = pd.read_sql(query, conn)

    # 显示数据
    st.write("数据库中的数据：")
    st.write("df_from_db")

    # 在这里添加句子标注的界面功能

    # # 关闭数据库连接
    # conn.close()


def tab2_fun():
    st.write("222")
    if st.button("重启通用工具服务"):
        st.write("fadf")


def run():
    tab1, tab2 = st.tabs(["查询相似病历", "..."])
    with tab1:
        tab1_fun()
    with tab2:
        tab2_fun()


if __name__ == "__main__":
    run()
