from lib.models.post import Post

class Comment(Post):
    def __init__(self, comment_id, post_id: int, user_id: int, content: str, created_on) -> None:
        self.comment_id = comment_id
        super().__init__(post_id, user_id, content, created_on)