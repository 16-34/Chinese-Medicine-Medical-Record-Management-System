import streamlit as st
import toml
import bcrypt
import os

from config import Config

# 登录页面
def login():
    st.title("用户登录")

    with st.form("login"):
        username = st.text_input("请输入用户名")
        password = st.text_input("请输入密码", type="password")

        if st.form_submit_button("登录"):
            if username in user_db:
                # 验证密码是否匹配
                hashed_password = user_db[username]["password"]
                if bcrypt.checkpw(
                    password.encode("utf-8"), hashed_password.encode("utf-8")
                ):
                    st.session_state["is_login"] = True
                    st.rerun()
                else:
                    st.error("用户名或密码错误，请重试")
            else:
                st.error("用户名或密码错误，请重试")


# 修改密码页面
def change_password():
    st.header("修改密码")
    st.divider()

    username = st.text_input("请输入用户名", value="admin")
    old_password = st.text_input("请输入旧密码", type="password")
    new_password = st.text_input("请输入新密码", type="password")
    confirm_password = st.text_input("请确认新密码", type="password")

    if st.button("确认修改"):
        if username in user_db:
            hashed_password = user_db[username]["password"]
            if bcrypt.checkpw(
                old_password.encode("utf-8"), hashed_password.encode("utf-8")
            ):
                if new_password == confirm_password:
                    new_hashed_password = bcrypt.hashpw(
                        new_password.encode("utf-8"), bcrypt.gensalt()
                    ).decode("utf-8")
                    user_db[username]["password"] = new_hashed_password
                    with open(Config.auth_db, "w") as f:
                        toml.dump(user_db, f)
                    st.success("密码修改成功")
                else:
                    st.error("新密码和确认密码不匹配")
            else:
                st.error("旧密码错误，请重试")
        else:
            st.warning("用户名不存在")

if not os.path.exists(Config.auth_db):
    with open(Config.auth_db, "w") as f:
        toml.dump(st.secrets["users"], f)

with open(Config.auth_db) as f:
    user_db = toml.load(f)

