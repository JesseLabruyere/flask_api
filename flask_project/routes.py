from flask import Flask, request, render_template, redirect, flash, url_for
import flask_project.json_web_token as jwt
import flask_project.database as db_manager
from flask_project.config_loader import ConfigLoader
from flask_project.forms import *

# load the configuration file
config = ConfigLoader.load_config()
# initialise the app
app = Flask(__name__)
# create a SQLAlchemy database object using the app object and database url
db = db_manager.init(app, config['mysql']['url'])
# initialise json web token security with the app object and secret key
jwt.init(app, config['authentication']['secret_key'], db)


# route protected by json web token
@app.route('/protected-jwt', methods=['GET', 'POST'])
@jwt.jwt_required()
def jwt_protected():
    return '%s' % jwt.current_identity


# route protected by json web token
@app.route('/register-user', methods=['GET', 'POST'])
@jwt.jwt_required()
@jwt.has_access_type('admin')
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


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)