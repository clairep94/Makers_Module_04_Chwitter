# Notes for Refactoring & Caching:

Currently storing all methods where the output is a list of that object class.
eg. get_all_likes_for_post is in LikeRepository, not PostRepository.
Storing in the 'many' end of the relationship

Currently prioritising minimising number of SQL queries -- will change to code-readability and code-refactoring if advised

## REFACTORING:

Future fork -- refactor post & comment to inherit from UserContent; refactor like & follow to inheriy from UserEvent

### FOR POST & COMMENT -- UserContent class;

```python
class BaseModel:
    def __init__(self, post_id, user_id, created_on, content):
        self.post_id = post_id
        self.user_id = user_id
        self.created_on = created_on
        self.content = content

class PostModel(BaseModel):
    def __init__(self, post_id, user_id, created_on, content):
        super().__init__(post_id, user_id, created_on, content)

class CommentModel(BaseModel):
    def __init__(self, comment_id, post_id, user_id, created_on, content):
        super().__init__(post_id, user_id, created_on, content)
        self.comment_id = comment_id

class BaseRepository:
    def __init__(self, db_connection, table_name):
        self.db_connection = db_connection
        self.table_name = table_name

    def select_all(self):
        query = f"SELECT * FROM {self.table_name}"
        return self.db_connection.execute(query)

class PostRepository(BaseRepository):
    def __init__(self, db_connection):
        super().__init__(db_connection, 'posts')

class CommentRepository(BaseRepository):
    def __init__(self, db_connection):
        super().__init__(db_connection, 'comments')
```

### FOR LIKE & FOLLOW -- UserEvent class:

```python
class BaseRepository:
    def __init__(self, connection, table_name):
        self._connection = connection
        self._table_name = table_name

    def create(self, **kwargs) -> int:
        # Construct the query template with placeholders
        query_template = f"INSERT INTO {self._table_name} ({', '.join(kwargs.keys())}) VALUES ({', '.join(['%s'] * len(kwargs))}) RETURNING id"
        
        # Execute the query with the provided keyword arguments
        rows = self._connection.execute(query_template, list(kwargs.values()))
        
        # Retrieve and return the newly created event_id
        return rows[0]['id']

class LikeRepository(BaseRepository):
    def like(self, user_id, post_id=None, comment_id=None) -> int:
        # Call the create method from the base class, passing in the specific keyword arguments
        return self.create(user_id=user_id, post_id=post_id, comment_id=comment_id)

class FollowRepository(BaseRepository):
    def follow(self, follower_id, followee_id) -> int:
        # Call the create method from the base class, passing in the specific keyword arguments
        return self.create(follower_id=follower_id, followee_id=followee_id)
```

## CACHING

Every time something is searched --> store in cache
When new get request is made:
- check cache first
- If none, then retrieve from DB and write to cache
- If yes, then retrieve from cache

Everything something is created --> update cache if in cache

Cache timeout every _____ amount of time? or drop longest ago item after ____ items?

```python
from flask import Flask, render_template
from flask_caching import Cache
from datetime import datetime, timedelta

app = Flask(__name)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Simulated database and data
class Post:
    def __init__(self, id, title):
        self.id = id
        self.title = title

class Comment:
    def __init__(self, id, post_id, text):
        self.id = id
        self.post_id = post_id
        self.text = text

posts = {
    1: Post(1, "Sample Post")
}

comments = {
    1: [Comment(1, 1, "Comment 1"), Comment(2, 1, "Comment 2")]
}

@app.route('/post/<int:post_id>/comments')
def get_comments(post_id):
    post = posts.get(post_id)
    if not post:
        return "Post not found", 404

    # Check if comments are in the cache
    cached_comments = cache.get(f'comments_post_{post_id}')
    if cached_comments is None:
        # If not in cache, fetch from the database
        comments_for_post = comments.get(post_id, [])
        # Store in the cache with no explicit timeout
        cache.set(f'comments_post_{post_id}', comments_for_post)

    return render_template('comments.html', comments=cached_comments)

# Simulated addition of new comments
@app.route('/add_comment/<int:post_id>/<text>')
def add_comment(post_id, text):
    new_comment = Comment(len(comments.get(post_id, []), post_id, text)
    comments[post_id].append(new_comment)
    
    # Update the cache when a new comment is added
    cache.set(f'comments_post_{post_id}', comments[post_id])
    
    return f"Added new comment: {text}"

if __name__ == '__main__':
    app.run()

```
