import streamlit as st
import pandas as pd
import sqlite3
from config import Config

# 查看所有数据
def view_all_data():
    st.header("数据总览")
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
        "record_time": "记录时间",
        "main_complaint": "主诉",
    }
    df_toshow = df[["name", "gender", "age", "record_time", "main_complaint"]].copy()
    df_toshow.rename(columns=columns_map, inplace=True)

    # 批量删除
    delete_btn = st.button("批量删除")
    event = st.dataframe(
        df_toshow,
        key="data",
        selection_mode=["multi-row"],
        on_select="rerun",
        use_container_width=True,
    )
    contain = st.container()
    selected_rows = event.selection["rows"]
    if delete_btn:
        if selected_rows:
            ids_to_delete = df.loc[selected_rows, "id"].tolist()
            cursor.executemany(
                "DELETE FROM patient_records WHERE id=?",
                [(id,) for id in ids_to_delete],
            )
            conn.commit()
            st.session_state["confirm"] = False
            st.rerun()
        else:
            st.warning("请先选择要删除的记录")

    conn.close()


view_all_data()
