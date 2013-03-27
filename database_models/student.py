from sqlalchemy import Column, Integer, String
import database

class Student(database.Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    school_id = Column(String(50), unique=True, nullable=False)

    def __init__(self, school_id):
        self.school_id = school_id

    def __repr__(self):
        return '<Student %r>' % (
            self.school_id
        )      
