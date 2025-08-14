import streamlit as st
import datetime
from models import User, Post, Like

def initialize_session_state():
    """
    Streamlit 세션 상태를 초기화하고 초기 데이터를 설정합니다.
    """
    if 'users' not in st.session_state:
        st.session_state.users = [
            User(1, 'user1', 'pass1'),
            User(2, 'user2', 'pass2')
        ]
    if 'posts' not in st.session_state:
        st.session_state.posts = [
            Post(1, 1, '첫 번째 게시물입니다!', datetime.datetime.now() - datetime.timedelta(hours=2)),
            Post(2, 2, '두 번째 게시물이네요. 반갑습니다.', datetime.datetime.now() - datetime.timedelta(hours=1))
        ]
    if 'likes' not in st.session_state:
        st.session_state.likes = [
            Like(1, 1, 2, datetime.datetime.now() - datetime.timedelta(hours=1.5))
        ]
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'page' not in st.session_state:
        st.session_state.page = "main_feed"
    if 'current_post_id' not in st.session_state:
        st.session_state.current_post_id = None