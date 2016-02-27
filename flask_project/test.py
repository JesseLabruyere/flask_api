from json_web_token import *

def create_test_data():

    # create AccessType objects and save them in the db
    access_type_admin = AccessType('admin')
    access_type_user = AccessType('user')
    db.session.add(access_type_admin)
    db.session.add(access_type_user)
    db.session.commit()

    # create User objects and save them in the db
    admin = User(None, 'admin@email.nl', 'admin', 'test', None, access_type_admin)
    user = User(None, 'user@email.nl', 'user', 'test', None, access_type_user)
    db.session.add(admin)
    db.session.add(user)
    db.session.commit()