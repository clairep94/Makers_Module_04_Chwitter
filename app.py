import os
from flask import Flask, request, render_template, redirect, url_for
from lib.database_connection import get_flask_database_connection


# Create a new Flask app
app = Flask(__name__)


# == Your Routes Here ==

# == Homepage == chwitter.com/ ==
@app.route('/', methods = ['GET'])
def landingpage():
    return render_template('landingpage.html')


### ===== POSTS ===== ####

# == ALL POSTS == chwitter.com/home ==

@app.route('/home', methods = ['GET'])
def home():
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return render_template('home.html', errors=None)

# == CREATE POST PAGE ==
@app.route('/posts/new', methods = ['GET'])
def create_post_page():
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return render_template('new_post.html', errors=None)

# == CREATE POST ==
@app.route('/posts', methods = ['POST'])
def create_post():
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return render_template('home.html', errors=None)

# == SHOW POST == chwitter.com/posts/<id> ==
@app.route('/posts/<id>', methods = ['GET'])
def show_post(id):
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return render_template('show_post.html', errors=None)

# == DELETE POST == chwitter.com/posts/<id>/delete --> chwitter.com/home ==
@app.route('/posts/<id>/delete', methods = ['POST'])
def delete_post(id):
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return redirect(url_for('home'))


# == UPVOTE/DOWNVOTE POST == page refresh
'''
When we click upvote or downvote, we upvote or downvote a tweet
We will refresh the page and see that the number of upvotes/downvotes has increase by 1.
** We can only upvote/downvote once.
'''
# TODO These only work on the homepage, not on the individual post page.
@app.route('/posts/<id>/upvote', methods = ['POST'])
def upvote_post(id):
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return redirect(request.referrer)

@app.route('/posts/<id>/downvote', methods = ['POST'])
def downvote_post(id):
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return redirect(request.referrer)


### ===== COMMENTS ===== ####

# == SHOW COMMENT == chwitter.com/posts/<post_id>/comments/<id> ==
@app.route('/posts/<post_id>/comments/<id>', methods = ['GET'])
def show_comment(post_id, id):
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return render_template('show_comment.html', errors=None)

# == DELETE POST == chwitter.com/<post_id>/comments/<id>/delete --> chwitter.com/home ==
@app.route('/posts/<post_id>/comments/<id>/delete', methods = ['POST'])
def delete_comment(post_id, id):
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return redirect(url_for('home')) #return home or parent post


# == UPVOTE/DOWNVOTE COMMENT == page refresh
'''
When we click upvote or downvote, we upvote or downvote a comment
We will refresh the page and see that the number of upvotes/downvotes has increase by 1.
** We can only upvote/downvote once.
'''
# TODO These only work on the homepage, not on the individual post page.
@app.route('/posts/<post_id>/comments/<id>/upvote', methods = ['POST'])
def upvote_comment(post_id, id):
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return redirect(request.referrer) #return home or parent post

@app.route('/posts/<post_id>/comments/<id>/downvote', methods = ['POST'])
def downvote_comment(post_id, id):
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return redirect(request.referrer) #return home or parent post





### ===== USERS ===== ####

# == USER == chwitter.com/users/<id> ==
'''
When we go to the link for single user, we should see:
We should see:
- Y Logo in H1
- link for the /home
- link for New Post
- link for Your Account

- A list of all posts in order of posting where earliest is first
- For each post:
    - Name (bold) @Username (italic) (link) - Xh ago or Xdays ago or date
    - Content
    - Upvotes
    - button for upvoting/downvoting
'''

# == ALL USERS ==
'''
When we go to the link for single user, we should see:
We should see:
- Y Logo in H1
- link for the /home
- link for New Post
- link for Your Account

- A list of all users. For each user:
    - Name (bold) @Username (italic) (link)

'''

# == CREATE NEW USER == chwitter.com/sign_up==
@app.route('/sign_up', methods = ['GET'])
def sign_up():
    return "<h1>TODO: CREATE SIGN UP PAGE<H1>"


# == SIGN IN == chwitter.com/login ==
@app.route('/login', methods = ['GET'])
def login():
    return "<h1>TODO: CREATE LOGIN PAGE<H1>"


# == SIGN OUT == chwitter.com/logout ==




# == Example Code Below ==

# GET /emoji
# Returns a smiley face in HTML
# Try it:
#   ; open http://localhost:5001/emoji
@app.route('/emoji', methods=['GET'])
def get_emoji():
    # We use `render_template` to send the user the file `emoji.html`
    # But first, it gets processed to look for placeholders like {{ emoji }}
    # These placeholders are replaced with the values we pass in as arguments
    return render_template('emoji.html', emoji=':)')

# This imports some more example routes for you to see how they work
# You can delete these lines if you don't need them.
from example_routes import apply_example_routes
apply_example_routes(app)

# == End Example Code ==

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
