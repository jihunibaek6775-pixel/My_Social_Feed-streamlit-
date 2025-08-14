import datetime

class User:
    """사용자 정보를 담는 클래스입니다."""
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

class Post:
    """게시글 정보를 담는 클래스입니다."""
    def __init__(self, post_id, user_id, content, timestamp, is_retweet=False, original_post_id=None):
        self.post_id = post_id                  # 고유 게시글 ID
        self.user_id = user_id                  # 게시글 작성자 ID
        self.content = content                  # 게시글 내용
        self.timestamp = timestamp              # 게시글 작성 시간
        self.is_retweet = is_retweet            # 리트윗 여부
        self.original_post_id = original_post_id  # 리트윗된 원본 게시글 ID

class Like:
    """좋아요 정보를 담는 클래스입니다."""
    def __init__(self, like_id, post_id, user_id, timestamp):
        self.like_id = like_id
        self.post_id = post_id
        self.user_id = user_id
        self.timestamp = timestamp