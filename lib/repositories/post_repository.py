from lib.models.post import Post
from lib.repositories.hashtag_repository import HashtagRepository
from datetime import datetime

class PostRepository:
    def __init__(self, connection):
        self._connection = connection

    # ========= BASIC METHODS ==================
    # all posts
    '''
    When we call all, we get all posts in our db
    '''
    def all(self) -> list[Post]:
        rows = self._connection.execute('SELECT * FROM posts')
        posts = []
        for row in rows:
            post = Post(row['id'], row['user_id'], row['content'], row['created_on'])
            posts.append(post)
        return posts

    # ========= FIND ===================
    # find a post by id
    def find_by_id(self, post_id:int) -> Post:
        rows = self._connection.execute('SELECT * FROM posts WHERE id=%s'[post_id])
        row = rows[0]
        return Post(row['id'], row['user_id'], row['content'], row['created_on'])

    # # find by content, case sensitive, one string only - TODO ADD LATER AFTER WEBSITE DRAFT IS DONE.
    # def find_by_content(self, search_string:str) -> None or list[Post]:
    #     '''
    #     When we search for a post by content
    #     We see a list of all posts with the search string matching part of the content.
    #     '''
    #     rows = self._connection.execute('SELECT * FROM posts WHERE content LIKE %s'[search_string])
    #     posts = []
    #     for row in rows:
    #         post = Post(row['id'], row['user_id'], row['content'], row['created_on'])
    #         posts.append(post)
    #     return posts

    # find posts with matching hashtag
    def find_by_hashtag(self, hashtag:str) -> None or list[Post]:
        '''
        When we search for all posts with a hashtag title,
        We see a list of all posts with that hashtag
        '''
        '''
        When we search for all posts with a hashtag title that doesn't exist in the db
        We get 'No results'
        '''
        '''
        If there are no posts with this existing hashtag, we should get None or "" 
        '''
        # find if hashtag exists in db -- return None if not
        hashtag = hashtag.lower()
        hashtag_repo = HashtagRepository()
        hashtag_id = hashtag_repo.find_id_by_title(title=hashtag)
        if hashtag_id == None:
            return None
        # find a list of posts with the hashtag -- return None if empty list
        rows = self._connection.execute('SELECT posts.id as post_id, posts.user_id, posts.content, posts.created_on FROM posts JOIN tags_posts ON posts.id = tags_posts.post_id WHERE tags_posts.hashtag_id = %s' [hashtag_id])
        posts = []
        for row in rows:
            post = Post(row['post_id'], row['user_id'], row['content'], row['created_on'])
            posts.append(post)
        if posts == []:
            return None
        return posts

    # ========= CREATE ====================
    '''
    When we create content, we have to be logged in and the content entry has to be not empty, otherwise we generate errors.
    If we have any hashtags, we separate them into a list
    '''
    def check_content_valid_errors(self, user_id, content) -> bool:
        if user_id == None: #TODO guard this at login-required?
            return "Please log in to create a post."
        if content == "" or content == None:
            return "Post content cannot be empty."
        return None

    def create(self, user_id, content, created_on, hashtags=None) -> int:
        # Create the post
        created_on = datetime.now() #format may cause issues
        rows = self._connection.execute('INSERT INTO posts (user_id, content, created_on) VALUES (%s, %s, %s) RETURNING id', [user_id, content, created_on])
        post_id = rows[0]['id']
        # Keep check hashtag for valid and error, create hashtag and add hashtag to hashtag repo instead?
        # TODO Check steps for this when I make the create_post page.
        return post_id


    # =========== EDIT =====================
    # edit post
    # TODO ADD LATER AFTER WEBSITE DRAFT IS DONE.
    
    # =========== DELETE ===================
    # delete post -- deleting the post does not destroy the hashtags.
    


    # ========= DISPLAY ========================
    # calculate date for display
    # find user_data for display

    # ========= SORT ========================
    # sort posts by likes # TODO ADD LATER AFTER WEBSITE DRAFT IS DONE.
    # sort posts by date  # TODO ADD LATER AFTER WEBSITE DRAFT IS DONE.

    # ========= LIKES ============================    
    # like a post
    # unlike a post
    # check if user_id already liked this 
    # find users who liked this 

    # ========= COMMENTS ======================
    # reply to post -- create a comment
    # find_all_comments_for_post(post_id) --> comment_repository




