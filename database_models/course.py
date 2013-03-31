import database
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Course(database.Base):
    __tablename__ = 'courses'

    course_id = Column(String(20), primary_key=True)
    name = Column(String(100), nullable=False)
    assignments = relationship("Assignment")

    def __init__(self, course_id, course_name):
        self.course_id = course_id
        self.course_name = course_name

    def __repr__(self):
        return '<Course course_id=%r>' % (
            self.course_id
        )      
