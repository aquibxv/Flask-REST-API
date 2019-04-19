from models.users import UserModel
from werkzeug.security import safe_str_cmp

# function to return the user when username and password is entered in /auth
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

# function to match identity
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_userid(user_id)