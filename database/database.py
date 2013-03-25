from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def init(db_name = "easymarking", user=""):
    engine = create_engine('sqlite:///database.db')

    global session
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

    Base.query = session.query_property()
    Base.metadata.bind = engine
