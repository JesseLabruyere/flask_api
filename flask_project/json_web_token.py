from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash

# the SQLAlchemy database object that is used is stored here
db = None


# this class initialises the json web token security
class JWTInitializer(object):
    # initialize json web token and make the object global accessible (jwt)
    def __init__(self, app, secret, database):
        self.set_secret_key(app, secret)
        self.jwt = JWT(app, authenticate, identity)
        db = database
        global db

    # adding the secret key to app
    def set_secret_key(self, app, secret):
        app.config['SECRET_KEY'] = secret

    # getting the JWT object
    def get_jwt(self):
        return self.jwt


# the user class, SQLAlchemy orm class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    pw_hash = db.Column(db.String(120), unique=False)

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        # TODO safe enough?
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def __str__(self):
        return "User(id='%s')" % self.id


# class that contains some static query methods
class DataLoader(object):

    def __init__(self):
        pass

    @staticmethod
    def getUsers():
        users = User.query.all()
        return users


# the method that handles the authentication
def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user


# this method is used to get the current identity
def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()


# adds a single user to the db and returns a user object
def add_user(username, password):
    user = User(username, password)
    db.session.add(user)
    db.session.commit(user)
    return user
