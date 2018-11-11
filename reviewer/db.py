from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import current_app, g

def get_db():
    if 'db' not in g:
        print('new connection to db')
        engine = create_engine(current_app.config['DATABASE'])
        Session = sessionmaker(bind=engine)
        g.db = Session()
        
    return g.db

def close_db(e=None):
    print('Close db')
    db = g.pop('db', None)

    if db is not None:
        print('Remove session')
        db.close()
        db.get_bind().dispose()