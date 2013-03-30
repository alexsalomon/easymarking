from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import database

class Student(database.Base):
    __tablename__ = 'students'

    school_id = Column(String(50), primary_key=True)
    assignments = relationship("Assignment")

    def __init__(self, school_id):
        self.school_id = school_id

    def __repr__(self):
        return '<Student %r>' % (
            self.school_id
        )      
