from lib.models.post import Post

class Comment(Post):
    def __init__(self, comment_id, post_id: int, user_id: int, content: str, created_on) -> None:
        self.comment_id = comment_id
        Post.__init__(post_id, user_id, content, created_on)
    
    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Comment({self.comment_id}, User #{self.user_id} commented on Post #{self.post_id})"
