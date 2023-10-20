class Like:
    def __init__(self, like_id, user_id, post_id, comment_id) -> None:
        self.like_id = like_id
        self.user_id = user_id
        self.post_id = post_id #none if like is on a comment
        self.comment_id = comment_id #none if like is on a post.