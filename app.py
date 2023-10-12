import os
from flask import Flask, request, render_template
from lib.database_connection import get_flask_database_connection

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==

# == Homepage == chwitter.com/ ==
'''
When we go to the homepage
We should see the following text:

h1: Y 
h2: Happening now
h3: Join today.

[Create Account]<a href="/sign_up">

Already have an account?  
[Sign in] <a href="/sign_in">
'''


# == ALL TWEETS == chwitter.com/home ==
'''
When we go to all tweets
We should see:
- Y Logo in H1
- link for the /home
- link for New Post
- link for Your Account
- button for Sign out

- A list of all posts in order of posting where earliest is first
- For each post:
    - Name (bold) @Username (italic) - Xh ago or Xdays ago or date
    - Content
    - Upvotes
    - button for upvote/downvoting
'''

# == TWEET == chwitter.com/posts/<id> ==
'''
When we go to a single tweet
We should see:
- Y Logo in H1
- link for the /home
- link for New Post
- link for Your Account
- button for Sign out

<b>{Name}</b> @{Username} - {hours ago or date}h
{content}
{upvotes}

- button for delete
'''

# == DELETE TWEET == chwitter.com/posts/<id>/delete --> chwitter.com/home ==
'''
When we click delete for a single tweet
We see "tweet successfully deleted"
Then we see the homepage refreshed without this tweet
'''

# == UPVOTE/DOWNVOTE TWEET == page refresh
'''
When we click upvote or downvote, we upvote or downvote a tweet
We will refresh the page and see that the number of upvotes/downvotes has increase by 1.
** We can only upvote/downvote once.
'''



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

# == CREATE NEW USER ==

# == SIGN IN ==

# == SIGN OUT ==




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
