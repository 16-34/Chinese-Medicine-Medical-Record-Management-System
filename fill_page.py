import streamlit as st
import datetime
import sqlite3
from config import Config


# 保存数据到 SQLite 数据库
def save_to_db(data):
    conn = sqlite3.connect(Config.data_db)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO patient_records (
            name, gender, age, main_complaint, medical_history, past_history, 
            allergy_history, tongue_pulse, diagnosis, prescription, record_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            data["name"],
            data["gender"],
            data["age"],
            data["main_complaint"],
            data["medical_history"],
            data["past_history"],
            data["allergy_history"],
            data["tongue_pulse"],
            data["diagnosis"],
            data["prescription"],
            data["record_time"],
        ),
    )

    conn.commit()
    conn.close()


# 填写记录表单
def create_patient_form(cache_data):

    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("姓名", key="input_name", value=cache_data.get("name", ""))

    with col2:
        gender = st.selectbox(
            "性别",
            ["男", "女"],
            key="select_gender",
            index=0 if cache_data.get("gender", "男") == "男" else 1,
        )

    with col3:
        age = st.number_input(
            "年龄", min_value=0, step=1, key="input_age", value=cache_data.get("age", 0)
        )

    st.divider()

    main_complaint = st.text_area(
        "主诉",
        key="textarea_main_complaint",
        value=cache_data.get("main_complaint", ""),
    )

    medical_history = st.text_area(
        "现病史",
        key="textarea_medical_history",
        value=cache_data.get("medical_history", ""),
    )
    past_history = st.text_area(
        "既往史", key="textarea_past_history", value=cache_data.get("past_history", "")
    )
    allergy_history = st.text_area(
        "过敏史",
        key="input_allergy_history",
        value=cache_data.get("allergy_history", ""),
    )

    tongue_pulse = st.text_area(
        "舌脉象", key="input_tongue_pulse", value=cache_data.get("tongue_pulse", "")
    )
    diagnosis = st.text_area(
        "辩证", key="textarea_diagnosis", value=cache_data.get("diagnosis", "")
    )
    prescription = st.text_area(
        "处方", key="textarea_prescription", value=cache_data.get("prescription", "")
    )

    col1, col2 = st.columns(2)
    with col1:
        # 提交按钮
        submit_button = st.form_submit_button(label="提交")
    with col2:
        clear_button = st.form_submit_button(label="清空")

    if clear_button:
        st.session_state["form_data"] = {}
        st.rerun()

    # 提交时进行校验
    if submit_button:
        if not name.strip():
            st.error("姓名不能为空，请输入姓名。")
            return None

        st.session_state["edit_mode"] = False
        return {
            "name": name.strip(),
            "gender": gender,
            "age": age,
            "main_complaint": main_complaint.strip() or "无",
            "medical_history": medical_history.strip() or "无",
            "past_history": past_history.strip() or "无",
            "allergy_history": allergy_history.strip() or "无",
            "tongue_pulse": tongue_pulse.strip() or "无",
            "diagnosis": diagnosis.strip() or "无",
            "prescription": prescription.strip() or "无",
            "record_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    return None


def confirmation_page(data):
    st.write("请确认以下信息：")
    st.markdown(
        f"""
<center>

|姓名|性别|年龄|记录时间|
|:-:|:-:|:-:|:-:|
|{data['name']}|{data['gender']}|{data['age']}|{data['record_time']}|

</center>

**现病史**:\n\n\t {data['medical_history']}\n\n
**既往史**: \n\n\t {data['past_history']}\n\n
**过敏史**: \n\n\t {data['allergy_history']}\n\n
**舌脉象**: \n\n\t {data['tongue_pulse']}\n\n
**辩证**: \n\n\t {data['diagnosis']}\n\n
**处方**: \n\n\t {data['prescription']}\n\n
""",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("确认提交"):
            save_to_db(data)
            st.session_state["form_data"] = {}
            st.session_state["edit_mode"] = True
            st.rerun()

    with col2:
        if st.button("返回修改"):
            st.session_state["edit_mode"] = True
            st.rerun()


if "form_data" not in st.session_state:
    st.session_state["form_data"] = {}

if "edit_mode" not in st.session_state:
    st.session_state["edit_mode"] = True

st.header("病历填写")

if st.session_state["edit_mode"]:
    with st.form(key="patient_form"):
        form_data = create_patient_form(st.session_state["form_data"])
        if form_data:
            st.session_state["form_data"] = form_data
            st.rerun()
else:
    confirmation_page(st.session_state["form_data"])
