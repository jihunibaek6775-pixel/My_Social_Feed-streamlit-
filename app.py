# app.py (Streamlit 버전)
import streamlit as st
import pandas as pd
import datetime

# Streamlit 앱의 세션 상태를 초기화합니다.
if 'users' not in st.session_state:
    st.session_state.users = []
if 'posts' not in st.session_state:
    st.session_state.posts = []
if 'likes' not in st.session_state:
    st.session_state.likes = []
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# --- 데이터 모델 클래스 (간단하게 재구성) ---
class User:
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

class Post:
    def __init__(self, post_id, user_id, content, timestamp, is_retweet=False, original_post_id=None):
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.timestamp = timestamp
        self.is_retweet = is_retweet
        self.original_post_id = original_post_id
    
    def get_user_name(self):
        user = next((u for u in st.session_state.users if u.user_id == self.user_id), None)
        return user.username if user else "알 수 없음"

    def get_like_count(self):
        return sum(1 for like in st.session_state.likes if like.post_id == self.post_id)

class Like:
    def __init__(self, like_id, post_id, user_id, timestamp):
        self.like_id = like_id
        self.post_id = post_id
        self.user_id = user_id
        self.timestamp = timestamp

# --- 유틸리티 함수 ---
def save_data(key, data):
    st.session_state[key] = data

def load_data(key):
    return st.session_state[key]

# --- UI 컴포넌트 ---
def show_login_page():
    st.title("로그인")
    with st.form("login_form"):
        username = st.text_input("사용자 이름")
        password = st.text_input("비밀번호", type="password")
        submitted = st.form_submit_button("로그인")
        if submitted:
            user = next((u for u in st.session_state.users if u.username == username and u.password == password), None)
            if user:
                st.session_state.current_user = user
                st.success(f"환영합니다, {user.username}님!")
                st.experimental_rerun()
            else:
                st.error("사용자 이름 또는 비밀번호가 잘못되었습니다.")
    if st.button("회원가입"):
        st.session_state.page = "register"
        st.experimental_rerun()

def show_register_page():
    st.title("회원가입")
    with st.form("register_form"):
        username = st.text_input("사용자 이름")
        password = st.text_input("비밀번호", type="password")
        submitted = st.form_submit_button("회원가입")
        if submitted:
            users_data = load_data('users')
            new_user_id = len(users_data) + 1
            new_user = User(user_id=new_user_id, username=username, password=password)
            users_data.append(new_user)
            save_data('users', users_data)
            st.success("회원가입이 완료되었습니다. 로그인해 주세요.")
            st.session_state.page = "login"
            st.experimental_rerun()
    if st.button("로그인"):
        st.session_state.page = "login"
        st.experimental_rerun()

def show_main_feed():
    st.sidebar.title(f"환영합니다, {st.session_state.current_user.username}님!")
    if st.sidebar.button("로그아웃"):
        st.session_state.current_user = None
        st.experimental_rerun()
    if st.sidebar.button("새 게시물 작성"):
        st.session_state.page = "create_post"
        st.experimental_rerun()

    st.title("최신 게시물")
    posts = sorted(st.session_state.posts, key=lambda p: p.timestamp, reverse=True)
    
    for post in posts:
        st.markdown(f"**작성자:** {post.get_user_name()} - {post.timestamp}")
        st.write(post.content)
        st.write(f"❤️ **좋아요:** {post.get_like_count()}개")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("좋아요", key=f"like_{post.post_id}"):
                likes_data = load_data('likes')
                new_like_id = len(likes_data) + 1
                new_like = Like(like_id=new_like_id, post_id=post.post_id, user_id=st.session_state.current_user.user_id, timestamp=datetime.datetime.now().isoformat())
                likes_data.append(new_like)
                save_data('likes', likes_data)
                st.success("게시글에 좋아요를 눌렀습니다!")
                st.experimental_rerun()
        with col2:
            if st.button("리트윗", key=f"retweet_{post.post_id}"):
                posts_data = load_data('posts')
                new_post_id = len(posts_data) + 1
                new_post = Post(post_id=new_post_id, user_id=st.session_state.current_user.user_id, content=post.content, timestamp=datetime.datetime.now().isoformat(), is_retweet=True, original_post_id=post.post_id)
                posts_data.append(new_post)
                save_data('posts', posts_data)
                st.success("게시글을 리트윗했습니다!")
                st.experimental_rerun()
        st.markdown("---")

def show_create_post_page():
    st.title("새 게시물 작성")
    with st.form("create_post_form"):
        content = st.text_area("내용:", height=200)
        submitted = st.form_submit_button("게시")
        if submitted:
            posts_data = load_data('posts')
            new_post_id = len(posts_data) + 1
            new_post = Post(post_id=new_post_id, user_id=st.session_state.current_user.user_id, content=content, timestamp=datetime.datetime.now().isoformat())
            posts_data.append(new_post)
            save_data('posts', posts_data)
            st.success("게시물이 성공적으로 작성되었습니다!")
            st.session_state.page = "main_feed"
            st.experimental_rerun()
    if st.button("뒤로가기"):
        st.session_state.page = "main_feed"
        st.experimental_rerun()

# --- 페이지 라우팅 ---
if 'page' not in st.session_state:
    st.session_state.page = "main_feed"

if not st.session_state.current_user:
    if st.session_state.page == "register":
        show_register_page()
    else:
        show_login_page()
else:
    if st.session_state.page == "create_post":
        show_create_post_page()
    else:
        show_main_feed()