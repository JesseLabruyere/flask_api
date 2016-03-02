from flask_sqlalchemy import SQLAlchemy

db = None


def init(app, db_url):
    global db
    if db is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
        db = SQLAlchemy(app)

    return db
