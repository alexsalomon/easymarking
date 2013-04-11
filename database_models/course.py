import database
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database_models.professor import Professor
from database_models.assignment import Assignment

class Course(database.Base):
    __tablename__ = 'courses'

    course_id = Column(String(20), primary_key=True)
    name = Column(String(100), nullable=False)
    professor = relationship("Professor")
    assignments = relationship("Assignment")

    def __init__(self, course_id, course_name, professor=None):
        self.course_id = course_id
        self.name = course_name

        if professor is not None:
            self.professor.append(professor)

    def __repr__(self):
        return '<Course course_id=%r>' % (
            self.course_id
        )      
