import streamlit as st
import pandas as pd
from io import BytesIO
import sqlite3
from config import Config


# 导出数据为 Excel
def export_to_excel(df):
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, engine="openpyxl")

    excel_buffer.seek(0)
    st.download_button(
        "导出当前查询",
        excel_buffer,
        file_name="patient_record.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


# 查看记录
def view_records():
    st.header("病历查询")
    st.divider()

    conn = sqlite3.connect(Config.data_db)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patient_records")
    data = cursor.fetchall()

    if not data:
        st.error("没有可查看的记录。")
        return

    df = pd.DataFrame(
        data,
        columns=[
            "id",
            "name",
            "gender",
            "age",
            "main_complaint",
            "medical_history",
            "past_history",
            "allergy_history",
            "tongue_pulse",
            "diagnosis",
            "prescription",
            "record_time",
        ],
    )

    # 原始字段名和表头的映射
    columns_map = {
        "name": "姓名",
        "gender": "性别",
        "age": "年龄",
        "main_complaint": "主诉",
        "medical_history": "现病史",
        "past_history": "既往史",
        "allergy_history": "过敏史",
        "tongue_pulse": "舌脉象",
        "diagnosis": "辩证",
        "prescription": "处方",
        "record_time": "记录时间",
    }
    df.rename(columns=columns_map, inplace=True)

    # 搜索框
    col1, col2 = st.columns([1, 5])
    with col1:
        search_mode = st.selectbox("匹配模式", ["AND", "OR"])

    with col2:
        search_query_str = st.text_input("搜索记录", "")

    if search_query_str:
        search_query_ls = search_query_str.strip().split()  # 关键字列表
        # 逐行匹配所有关键字
        if search_mode == "AND":
            df = df[
                df.apply(
                    lambda row: all(
                        row.astype(str).str.contains(query, case=False, na=False).any()
                        for query in search_query_ls
                    ),
                    axis=1,
                )
            ]
        else:  # OR 模式
            df = df[
                df.apply(
                    lambda row: any(
                        row.astype(str).str.contains(query, case=False, na=False).any()
                        for query in search_query_ls
                    ),
                    axis=1,
                )
            ]

    # 以更美观的文本形式展示记录
    if not df.empty:
        export_to_excel(df)
        st.write(f"共找到 {df.shape[0]} 条记录。")
        for index, row in df.iterrows():
            with st.expander(f"{row['记录时间']} &emsp; {row['姓名']}"):
                st.markdown(
                    f"""
|姓名|性别|年龄|记录时间|
|:-:|:-:|:-:|:-:|
|{row['姓名']}|{row['性别']}|{row['年龄']}|{row['记录时间']}|

**主诉**:\n\n\t {row['主诉']}\n\n
**现病史**:\n\n\t {row['现病史']}\n\n
**既往史**: \n\n\t {row['既往史']}\n\n
**过敏史**: \n\n\t {row['过敏史']}\n\n
**舌脉象**: \n\n\t {row['舌脉象']}\n\n
**辩证**: \n\n\t {row['辩证']}\n\n
**处方**: \n\n\t {row['处方']}\n\n
"""
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("删除记录", key=f"button_delete_{index}"):
                        cursor.execute(
                            "DELETE FROM patient_records WHERE id=?", (row["id"],)
                        )
                        conn.commit()
                        st.success("记录已删除")
                        st.rerun()

                with col2:
                    if st.button("追加记录", key=f"button_append_{index}"):
                        st.session_state["form_data"] = {
                            "name": row["姓名"],
                            "gender": row["性别"],
                            "age": row["年龄"],
                            "main_complaint": row["主诉"],
                            "medical_history": row["现病史"],
                            "past_history": row["既往史"],
                            "allergy_history": row["过敏史"],
                            "tongue_pulse": row["舌脉象"],
                            "diagnosis": row["辩证"],
                            "prescription": row["处方"],
                        }
                        st.session_state["edit_mode"] = True
                        st.switch_page("fill_page.py")

    else:
        st.write("没有符合条件的记录。")

    conn.close()


view_records()
