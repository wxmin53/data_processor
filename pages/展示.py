import streamlit as st


def tab1_fun():
    st.write("!!!!")


def tab2_fun():
    st.write("222")
    if st.button("重启通用工具服务"):
        st.write("fadf")


def run():
    tab1, tab2 = st.tabs(["ha", "..."])
    with tab1:
        tab1_fun()
    with tab2:
        tab2_fun()


if __name__ == "__main__":
    run()