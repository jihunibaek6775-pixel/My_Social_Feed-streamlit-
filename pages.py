# pages.py
import streamlit as st
import datetime
from models import User, Post, Like

def show_login_page():
    """로그인 페이지를 렌더링합니다."""
    st.title("로그인")
    with st.form("login_form"):
        st.header("로그인")
        username = st.text_input("사용자 이름")
        password = st.text_input("비밀번호", type="password")
        submitted = st.form_submit_button("로그인")

        if submitted:
            user = next((u for u in st.session_state.users if u.username == username and u.password == password), None)
            if user:
                st.session_state.current_user = user
                st.session_state.page = "main_feed"
                st.rerun()
            else:
                st.error("사용자 이름 또는 비밀번호가 잘못되었습니다. 계정이 존재하지 않습니다.")

    st.markdown("---")
    st.info("아직 계정이 없으신가요?")
    if st.button("회원가입 페이지로 이동"):
        st.session_state.page = "register"
        st.rerun()


def show_register_page():
    """회원가입 페이지를 렌더링합니다."""
    st.title("회원가입")
    with st.form("register_form"):
        st.header("새 계정 생성")
        username = st.text_input("사용자 이름")
        password = st.text_input("비밀번호", type="password")
        submitted = st.form_submit_button("회원가입")

        if submitted:
            if any(u.username == username for u in st.session_state.users):
                st.error("이미 존재하는 사용자 이름입니다.")
            else:
                new_user_id = len(st.session_state.users) + 1
                new_user = User(user_id=new_user_id, username=username, password=password)
                st.session_state.users.append(new_user)
                st.success("회원가입이 완료되었습니다. 로그인해 주세요.")
                st.session_state.page = "login"
                st.rerun()
    
    st.markdown("---")
    if st.button("로그인 페이지로 돌아가기"):
        st.session_state.page = "login"
        st.rerun()


def show_main_feed():
    """메인 피드 페이지를 렌더링합니다."""
    with st.sidebar:
        st.title("내 정보")
        st.write(f"**환영합니다, {st.session_state.current_user.username}님!**")

        st.markdown("---")
        if st.button("새 게시물 작성", key="create_post_btn"):
            st.session_state.page = "create_post"
            st.rerun()
        if st.button("로그아웃", key="logout_btn"):
            st.session_state.current_user = None
            st.session_state.page = "login"
            st.rerun()

    st.title("최신 게시물")
    posts = sorted(st.session_state.posts, key=lambda p: p.timestamp, reverse=True)
    
    for post in posts:
        with st.container(border=True):
            user = next((u for u in st.session_state.users if u.user_id == post.user_id), None)
            
            # 리트윗 게시물인 경우 UI 변경
            if post.is_retweet:
                original_post = next((p for p in st.session_state.posts if p.post_id == post.original_post_id), None)
                if original_post:
                    original_username = next((u.username for u in st.session_state.users if u.user_id == original_post.user_id), "알 수 없음")
                    st.markdown(f"🔁 **{user.username}님이 리트윗했습니다.**")
                    with st.expander(f"**원본 게시글 by @{original_username}**", expanded=True):
                        st.write(f"**내용:** {original_post.content}")
                else:
                    st.markdown(f"🔁 **{user.username}님이 리트윗한 게시글 (원본 삭제됨)**")
                    st.write("원본 게시글을 찾을 수 없습니다.")
            else:
                st.markdown(f"**작성자:** {user.username if user else '알 수 없음'}")
                st.write(f"**내용:** {post.content}")

            st.markdown(f"<small>작성 시간: {post.timestamp}</small>", unsafe_allow_html=True)
            like_count = len([l for l in st.session_state.likes if l.post_id == post.post_id])
            st.write(f"❤️ **좋아요:** {like_count}개")

            if st.button("게시글 상세 보기", key=f"view_post_{post.post_id}"):
                st.session_state.page = "view_post"
                st.session_state.current_post_id = post.post_id
                st.rerun()


def show_view_post_page():
    """게시글 상세 보기 페이지를 렌더링합니다."""
    post_id = st.session_state.current_post_id
    post = next((p for p in st.session_state.posts if p.post_id == post_id), None)
    
    if not post:
        st.error("게시물을 찾을 수 없습니다.")
        if st.button("메인 피드로 돌아가기"):
            st.session_state.page = "main_feed"
            st.rerun()
        return

    st.title("게시글 상세 보기")
    with st.container(border=True):
        user = next((u for u in st.session_state.users if u.user_id == post.user_id), None)
        st.markdown(f"**작성자:** {user.username if user else '알 수 없음'}")
        st.markdown(f"**내용:** {post.content}")
        st.markdown(f"<small>작성 시간: {post.timestamp}</small>", unsafe_allow_html=True)

        like_count = len([l for l in st.session_state.likes if l.post_id == post.post_id])
        st.write(f"❤️ **좋아요:** {like_count}개")

        col1, col2 = st.columns(2)
        with col1:
            is_liked = any(l.post_id == post_id and l.user_id == st.session_state.current_user.user_id for l in st.session_state.likes)
            if is_liked:
                if st.button("좋아요 취소", key=f"unlike_{post_id}"):
                    st.session_state.likes = [l for l in st.session_state.likes if not (l.post_id == post_id and l.user_id == st.session_state.current_user.user_id)]
                    st.rerun()
            else:
                if st.button("좋아요", key=f"like_{post_id}"):
                    new_like_id = len(st.session_state.likes) + 1
                    new_like = Like(new_like_id, post_id, st.session_state.current_user.user_id, datetime.datetime.now())
                    st.session_state.likes.append(new_like)
                    st.rerun()

        with col2:
            if st.button("리트윗", key=f"retweet_{post_id}"):
                posts_data = st.session_state.posts
                new_post_id = len(posts_data) + 1
                new_post = Post(post_id=new_post_id, user_id=st.session_state.current_user.user_id, content=post.content, timestamp=datetime.datetime.now(), is_retweet=True, original_post_id=post_id)
                posts_data.append(new_post)
                st.success("게시글을 리트윗했습니다!")
                st.session_state.page = "main_feed"
                st.rerun()

    st.markdown("---")
    if st.button("메인 피드로 돌아가기"):
        st.session_state.page = "main_feed"
        st.rerun()


def show_create_post_page():
    """새 게시물 작성 페이지를 렌더링합니다."""
    st.title("새 게시물 작성")
    with st.form("create_post_form"):
        content = st.text_area("내용:", height=200)
        submitted = st.form_submit_button("게시")

        if submitted:
            if content:
                new_post_id = len(st.session_state.posts) + 1
                new_post = Post(post_id=new_post_id, user_id=st.session_state.current_user.user_id, content=content, timestamp=datetime.datetime.now())
                st.session_state.posts.append(new_post)
                st.success("게시물이 성공적으로 작성되었습니다!")
                st.session_state.page = "main_feed"
                st.rerun()
            else:
                st.error("내용을 입력해 주세요.")
    
    st.markdown("---")
    if st.button("메인 피드로 돌아가기"):
        st.session_state.page = "main_feed"
        st.rerun()