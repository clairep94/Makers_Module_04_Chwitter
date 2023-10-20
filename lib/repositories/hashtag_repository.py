from lib.models.post import Post
from lib.models.hashtag import Hashtag

class HashtagRepository:
    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection
    
    # == ALL HASHTAGS ================
    '''
    When we call all, we get all hashtags in our db
    '''
    def all(self) -> list[Hashtag]:
        rows = self._connection.execute('SELECT * FROM hashtags')
        hashtags = []
        for row in rows:
            hashtag = Hashtag(row['id'], row['title'])
            hashtags.append(hashtag)
        return hashtags
    
    # == FIND HASHTAG ================
    # Find hashtag by ID
    '''
    We can find the hashtag by the hashtag_id 
    '''
    def find_by_id(self, hashtag_id:int) -> Hashtag:
        rows = self._connection.execute('SELECT * FROM hashtags WHERE id=%s', [hashtag_id])
        row = rows[0]
        return Hashtag(row['id'], row['title'])

    # Find ID by hashtag title
    '''
    We can find the hashtag_id by a potential hashtag title. If it does not exist, we get None.
    '''
    def find_id_by_title(self, title:str) -> int or None:
        title = title.lower()
        rows = self._connection.execute('SELECT * FROM hashtags WHERE title=%s', [title])
        if rows == []:
            return None
        row = rows[0]
        return row['id']

    # == CREATE NEW HASHTAG ============
    '''
    When we have the user creates a post with a non-empty hashtag entry
    We can check if the hashtag is already in the DB
    If it is not, we add it to hashtags
    We can see it in hashtags.all
    '''
    # Check if the tag field is empty & if not, if the tag already exists:
    # If none, the tag is valid
    # If not none, generates a list of errors.
    def check_if_new_and_valid(self, new_tag:str) -> list or None:
        if new_tag == None or new_tag == "":
            return False
        new_tag = new_tag.lower() #all hashtags are lowercase?
        same_entry = self.find_id_by_title(new_tag)
        if same_entry != None:
            return False
        return True

    # Generate list of errors -TODO

    # if check_if_new_and_valid(new_tag):
    def create(self, new_tag:str) -> int:
        new_tag = new_tag.lower()
        rows = self._connection.execute('INSERT INTO hashtags (title) VALUES (%s) RETURNING id', [new_tag])
        hashtag_id = rows[0]['id']
        return hashtag_id
    
    # == DELETE A HASHTAG ===============
    
    # Delete a hashtag
    '''
    When we delete a hashtag,
    It should no longer by in all hashtags
    '''
    '''
    INTEGRATION WITH POST REPO:
    When we delete a hashtag,
    It should be removed from posts that had this hashtag
    '''
    def delete(self, hashtag_id:int) -> None:
        self._connection.execute('DELETE FROM hashtags WHERE id = %s', [hashtag_id])
        return None
    
########################################################

    # == POSTS INTEGRATION ===============

    # Add hashtag to post
    '''
    When we add a hashtag to a post
    We see it in all_hashtags_for_post()
    '''
    def add_to_post(self, hashtag_id:int, post_id:int) -> None:
        self._connection.execute('INSERT INTO hashtags_posts (hashtag_id, post_id) VALUES (%s, %s)', [hashtag_id, post_id])
        return None
    
    # Delete hashtag from post
    '''
    When we delete a hashtag from a post
    We no longer see it in all_hashtags_for_post()
    '''
    def delete_from_post(self, hashtag_id:int, post_id:int) -> None:
        self._connection.execute('DELETE FROM hashtags_posts WHERE hashtag_id = %s AND post_id = %s', [hashtag_id, post_id])
        return None


    # Show all hashtags for one post -- move to posts?
    '''
    We can find a list of all hashtags for a post
    '''
    '''
    If there are no hashtags for the post, we should see "" or None
    '''

    def all_for_post(self, post_id:int) -> None or list[Hashtag]:
        rows = self._connection.execute('SELECT hashtags.id as hashtag_id, hashtags.title FROM hashtags JOIN hashtags_posts ON hashtags.id = hashtags_posts.hashtag_id WHERE hashtags_posts.post_id = %s', [post_id])
        hashtags = []
        for row in rows:
            hashtag = Hashtag(row['hashtag_id'], row['title'])
            hashtags.append(hashtag)
        if hashtags == []:
            return None #decide if None or [] is better for later purposes.
        return hashtags


    # Find all posts with a certain hashtag -- move to posts?
    '''
    We can find a list of all post id's with a certain hashtag
    If the hashtag doesn't exist, we get None
    If no posts are attached to the hashtag, we get None
    '''
    def find_all_posts_by_hashtag(self, hashtag_string:str) -> None or list[int]:
        hashtag_id = self.find_id_by_title(hashtag_string)
        if hashtag_id == None:
            return None
        rows = self._connection.execute('SELECT post_id, user_id, content, created_on FROM posts JOIN hashtags_posts ON posts.id = hashtags_posts.post_id WHERE hashtags_posts.hashtag_id = %s', [hashtag_id])
        posts = []
        for row in rows:
            post = row['post_id']
            #post = Post(row['post_id'], row['user_id], row['content'], row['created_on'])
            posts.append(post)
        if posts == []:
            return None #decide if None or [] is better for later purposes.
        return posts #decide if list[int] or list[Post] later

    # Generate Hashtags function -- create list of hashtags from list of hashtag_ids