from lib.user import User
from datetime import datetime

class UserRepository:
    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # == ALL USERS =============
    # Retrieve all registered users from db
    def all(self) -> list[User]:
        rows = self._connection.execute('SELECT * FROM users')
        users = []
        for row in rows:
            user = User(row['user_id'], row['email'], row['password'], row['handle'], row['name'],
                        row['joined_on'], row['followers'], row['following'], row['posts'],
                        row['replies'], row['likes'])
            users.append(user)
        return users

    # == FIND SINGLE USER =============

    # Find a single user by id
    def find(self, user_id:int) -> User:
        rows = self._connection.execute('SELECT * FROM users WHERE user_id =%s', [user_id])
        row = rows[0]
        return User(row['user_id'], row['email'], row['password'], row['handle'], row['name'],
                        row['joined_on'], row['followers'], row['following'], row['posts'],
                        row['replies'], row['likes'])

    # Find a single user_id by username 
    def find_id_by_handle(self, handle:str) -> int or None:
        rows = self._connection.execute('SELECT user_id FROM users WHERE handle = %s', [handle])
        user_id = rows[0] 
        return user_id #int if handle exists, None if not

    # == CREATE NEW USER & ERRORS =============

    # Create a new user
    def create(self, user:User) -> int:
        user.joined_on = datetime.now()
        rows = self._connection.execute('INSERT INTO users (email, password, handle, name, joined_on) VALUES (%s, %s, %s, %s, %s) RETURNING user_id',
                                        [user.email, user.password, user.handle, user.name, user.joined_on])
        user_id = rows[0]['user_id'] # SQL creates user_id in serial when a new row is inserted
        return user_id

    # == DELETE A USER =============

    # Delete a user by id
    def delete(self, user_id) -> None:
        self._connection.execute('DELETE FROM users WHERE user_id = %s', [user_id])
        return None
    
    #TODO potentially change this depending on order of what to check
    # Check if new user's desired handle or email have previously been used:
    # Return list of errors to display or empty list
    def check_registration_duplicate(self, handle:str, email:str) -> list:
        errors = []
        same_email_rows = self._connection.execute('SELECT user_id FROM users WHERE email = %s', [email])
        if same_email_rows != None:
            errors.append("Email is already registered with an account. Please login.")
        same_handle_rows = self._connection.execute('SELECT user_id FROM users WHERE handle =%s', [handle])
        if same_handle_rows != None:
            errors.append("Handle is already registered with an account. Please login or pick another handle.")
        return errors

    # Check that all entries are valid
    def is_valid(self, email:str, password:str, handle:str, name:str) -> list:
        errors = []
        if email == None or email == "":
            errors.append("Email cannot be empty")
        elif "@" not in email: #TODO Refine this!
            errors.append("Invalid email address")

        if password == None or password == "":
            errors.append("Password cannot be empty")
        elif len(password) <= 8:
            errors.append("Password must be 8 chars or longer")
        # TODO: Add additional rules for password such as needing one num, one special char, one lowercase letter, one upper case letter

        if handle == None or handle == "":
            errors.append("Handle cannot be empty")
        if name == None or name == "":
            errors.append("Name cannot be empty")
        return errors

    # Create printable errors string
    def generate_errors(self, duplicates_errors, validity_errors) -> None or str:
        if duplicates_errors == [] and validity_errors == []:
            return None
        all_errors = duplicates_errors + validity_errors
        return ", ".join(all_errors)
