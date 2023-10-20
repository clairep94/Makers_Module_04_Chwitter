class Post:
    def __init__(self, post_id:int, user_id:int, content:str, created_on) -> None:
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.created_on = created_on
        print(f"created_on data type:{type(self.created_on)}")
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Post({self.post_id}, {self.user_id}, {self.content}, {self.created_on})"
    
