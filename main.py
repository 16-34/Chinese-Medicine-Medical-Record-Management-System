import streamlit as st
from auth import change_password, login
import sqlite3

from config import Config


def create_record_table():
    conn = sqlite3.connect(Config.data_db)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS patient_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            gender TEXT,
            age INTEGER,
            main_complaint TEXT,
            medical_history TEXT,
            past_history TEXT,
            allergy_history TEXT,
            tongue_pulse TEXT,
            diagnosis TEXT,
            prescription TEXT,
            record_time TEXT
        )
    """
    )

    conn.commit()
    conn.close()

create_record_table()

st.set_page_config(
    page_title="中医病历管理系统",
    layout="centered",
    initial_sidebar_state="auto",
)


if st.session_state.get("is_login", False):

    pg = st.navigation(
        {
            "中医病历管理系统": [
                st.Page("./fill_page.py", title="填写", icon=":material/edit:"),
                st.Page("./query_page.py", title="查询", icon=":material/search:"),
                st.Page("./data_page.py", title="数据表", icon=":material/table_view:"),
            ],
            "用户管理": [
                st.Page(change_password, title="修改密码", icon=":material/lock:"),
            ],
        }
    )
    pg.run()
else:
    login()
