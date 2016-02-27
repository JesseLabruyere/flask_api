from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash

# the SQLAlchemy database object that is used is stored here
db = None
# the jwt object
jwt = None


# initialises the json web token security
def init(app, secret, database):
    set_secret_key(app, secret)
    jwt = JWT(app, authenticate, identity)
    global jwt
    db = database
    global db


# adding the secret key to app
def set_secret_key(app, secret):
    app.config['SECRET_KEY'] = secret


# the user class, SQLAlchemy orm class
class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    access_type_id = db.Column(db.Integer, db.ForeignKey('access_type.id'), nullable=False)
    access_type = db.relationship('AccessType', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, id, email, username, password, access_type_id, access_type):
        self.id = id
        self.email = email
        self.username = username
        self.set_password(password)
        self.access_type_id = access_type_id
        self.access_type = access_type

    def set_password(self, password):
        # TODO safe enough?
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r, %r>' % self.id, self.username


# this class describes the access type that can be linked to users
class AccessType(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r, %r>' % self.id, self.name


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


# adds a single user to the db and returns a User object
def add_user(username, password):
    user = User(username, password)
    db.session.add(user)
    db.session.commit(user)
    return user


# method that checks if the current User complies with the given access types
def has_access_type(access_type):
    user_access_type = current_identity.access_type
    # check if a list of requirements is given
    if isinstance(access_type, list):
        for item in access_type:
            if user_access_type == item:
                return True
        return False
    else:
        return user_access_type == access_type
