# app.py
import streamlit as st
from data_manager import initialize_session_state
from pages import (
    show_login_page,
    show_register_page,
    show_main_feed,
    show_view_post_page,
    show_create_post_page
)

# 세션 상태를 초기화합니다.
initialize_session_state()

# 현재 로그인된 사용자가 없으면 로그인 또는 회원가입 페이지를 표시합니다.
if not st.session_state.current_user:
    if st.session_state.page == "register":
        show_register_page()
    else:
        show_login_page()
# 로그인된 사용자가 있으면 페이지 상태에 따라 적절한 화면을 표시합니다.
else:
    if st.session_state.page == "create_post":
        show_create_post_page()
    elif st.session_state.page == "view_post":
        show_view_post_page()
    else:
        show_main_feed()