import flask_project.json_web_token as jwt
from flask import Flask
from flask_project import database as db_manager
from flask_project.config_loader import ConfigLoader

# load the configuration file
config = ConfigLoader.load_config()

# initialise the app
app = Flask(__name__)

# create a SQLAlchemy database object using the app object and database url
db = db_manager.init(app, config['mysql']['url'])

# initialise json web token security with the app object and secret key
jwt_initializer = jwt.JWTInitializer(app, config['authentication']['secret_key'], db)


# route protected by json web token
@app.route('/protected-jwt')
@jwt.jwt_required()
def jwt_protected():
    return '%s' % jwt.current_identity


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