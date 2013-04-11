from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from sqlalchemy.ext.declarative import declarative_base
from transaction import commit_on_success

Base = declarative_base()

def init(db_name = "database"):
	engine = create_engine('sqlite:///database_models/%s.db' % (db_name))

	global session
	session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

	Base.query = session.query_property()
	Base.metadata.create_all(bind=engine)

@event.listens_for(mapper, 'init')
def auto_add_to_session(target, args, kwargs):
	""" Automatically add target to session """
	session.add(target)

@commit_on_success
def empty_database():
	for table in reversed(Base.metadata.sorted_tables):
		session.execute(table.delete())
