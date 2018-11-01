from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import current_app, g

def get_db():
    if 'db' not in g:
        engine = create_engine(current_app.config['DATABASE'])
        g.db = scoped_session(sessionmaker(bind=engine))
        
    return g.db