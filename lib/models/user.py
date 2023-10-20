from datetime import datetime
class User:
    # We initialise with all of our attributes
    # Each column in the table should have an attribute here
    def __init__(self, user_id:int, email:str, password:str, handle:str, name:str, joined_on:datetime=None):
        self.user_id = user_id # serial generation on init
        # Registration:
        self.email = email # hidden
        # TODO: Something with hashing password here, or in user_repository#Create
        self.password = password #figure out how to hide this
        self.handle = handle # @AOC
        self.name = name # Alexandria Ocasio-Cortez
        self.joined_on = joined_on # Joined April 2017; datetime.date on user_repository#Create
        ## User activity -- TODO MOVE TO USER_REPOSITORY:
        # self.followers = followers # 11 following, clickable list of Users 
        # self.following = following # 1 follower, clickable list of Users
        # self.posts = posts # clickable link to list of posts
        # self.replies = replies # clickable link to list of replies
        # self.likes = likes # clickable link to list of likes

    # This method allows our tests to assert that the objects it expects
    # are the objects we made based on the database records.
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # This method makes it look nicer when we print an Users
    def __repr__(self):
        return f"User({self.user_id}, {self.name}, {self.handle})"
