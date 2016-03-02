from config.config_loader import ConfigLoader
from flask import Flask, request, render_template, redirect, flash, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms_alchemy import ModelForm
from functools32 import wraps


''' Config'''


# load the configuration file
config = ConfigLoader.load_config()


''' Flask'''


# initialise the app
app = Flask(__name__)


''' DB '''


def create_db(flask_app, db_url):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    sql_alchemy_db = SQLAlchemy(app)
    return sql_alchemy_db


# create a SQLAlchemy database object using the app object and database url
db = create_db(app, config['mysql']['url'])


''' JWT '''


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
        return '<AccessType %r, %r>' % self.id, self.name


class UserForm(ModelForm):
    template = 'templates/forms/user.html'

    class Meta:
        model = User
        include = ['access_type_id']


# adding the secret key to app
def set_secret_key(app, secret):
    app.config['SECRET_KEY'] = secret


# the method that handles the authentication
def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user


# this method is used to get the current identity
def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()


# method that checks if the current User complies with the given access types
def has_access_type(access_type):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_access_type = current_identity.access_type.name
            # check if a list of requirements is given
            if isinstance(access_type, list):
                for item in access_type:
                    if user_access_type == item:
                        return
                abort(403)
            else:
                if user_access_type == access_type:
                    return
                else:
                    abort(403)
        return decorated_function
    return decorator


# initialises the json web token security
def create_jwt(flask_app, secret):
    set_secret_key(flask_app, secret)
    return JWT(flask_app, authenticate, identity)


# initialise json web token security with the app object and secret key
jwt = create_jwt(app, config['authentication']['secret_key'])


''' Test '''


def create_test_data():

    # create AccessType objects and save them in the db
    access_type_admin = AccessType('admin')
    access_type_user = AccessType('user')
    db.session.add(access_type_admin)
    db.session.add(access_type_user)
    db.session.commit()

    # create User objects and save them in the db
    admin = User(None, 'admin@email.nl', 'admin', 'test', access_type_admin.id, access_type_admin)
    user = User(None, 'user@email.nl', 'user', 'test', access_type_user.id, access_type_user)
    db.session.add(admin)
    db.session.add(user)
    db.session.commit()

create_test_data()


''' Routes '''


# route protected by json web token
@app.route('/protected-jwt', methods=['GET', 'POST'])
@jwt_required()
def jwt_protected():
    return '%s' % current_identity


# route protected by json web token
@app.route('/register-user', methods=['GET', 'POST'])
@jwt_required()
@has_access_type('admin')
def add_user():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(None, form.email.data, form.username.data, form.password.data, None)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('jwt_protected'))
    return render_template(form.template, form=form)


# regular route
@app.route('/')
def hello_world():
    return 'Hello World! from ' + config['mysql']['host']


# regular route
@app.route('/test')
def test():
    return 'test'


''' initialize '''
if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)