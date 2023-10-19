# Storing the model class in the same file as this model class is simple and to save space.
class Hashtag:
    def __init__(self, hashtag_id:int, title:str):
        self.hashtag_id = hashtag_id
        self.title = title

    # This method allows our tests to assert that the objects it expects
    # are the objects we made based on the database records.
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # This method makes it look nicer when we print an Users
    def __repr__(self):
        return f"Hashtag({self.hashtag_id}, {self.title})"


#######################################################################

# from lib.post import Post

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
    def check_if_new_and_valid(self, new_tag:str) -> bool:
        if new_tag == None or new_tag == "":
            return False
        new_tag = new_tag.lower() #all hashtags are lowercase?
        same_entry = self.find_id_by_title(new_tag)
        if same_entry != None:
            return False
        return True

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

    # Search for all posts with a hashtag #TODO -- when posts is written
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
    # def all_posts_by_hashtag(self, hashtag_title:str) -> None or list[Post]:
    #     hashtag_id = self.find_id_by_title(title=hashtag_title)
    #     if hashtag_id == None:
    #         return None
    #     rows = self._connection.execute('SELECT posts.id as post_id, posts.user_id, posts.content, posts.created_on FROM posts JOIN tags_posts ON posts.id = tags_posts.post_id WHERE tags_posts.hashtag_id = %s' [hashtag_id])
    #     posts = []
    #     for row in rows:
    #         post = Post(row['post_id'], row['user_id'], row['content'], row['created_on'])
    #         posts.append(post)
    #     if posts == []:
    #         return None
    #     return posts

    # Show all hashtags for one post -- move to posts?
    '''
    We can find a list of all hashtags for a post
    '''
    '''
    If there are no hashtags for the post, we should see "" or None
    '''

    def all_hashtags_for_post(self, post_id:int) -> None or list[Hashtag]:
        rows = self._connection.execute('SELECT hashtags.id as hashtag_id, hashtags.title FROM hashtags JOIN hashtags_posts ON hashtags.id = hashtags_posts.hashtag_id WHERE hashtags_posts.post_id = %s', [post_id])
        hashtags = []
        for row in rows:
            hashtag = Hashtag(row['hashtag_id'], row['title'])
            hashtags.append(hashtag)
        if hashtags == []:
            return None
        return hashtags
