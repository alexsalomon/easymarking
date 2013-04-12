import database
from sqlalchemy import Column, Integer, String

class Professor(database.Base):
    __tablename__ = 'professors'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    email = Column(String(254))

    @classmethod
    def get(cls, prof_name):
        return cls.query.filter_by(name=prof_name).first()

    def __init__(self, name, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Professor id=%r name=%r>' % (
            self.id,
            self.name
        )     
