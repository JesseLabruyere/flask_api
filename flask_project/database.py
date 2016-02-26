from flask_sqlalchemy import SQLAlchemy


def init(app, db_url):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    db = SQLAlchemy(app)
    return db
