import database
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from database_models.professor import Professor
from database_models.assignment import Assignment

class Course(database.Base):
    __tablename__ = 'courses'

    course_id = Column(String(20), primary_key=True)
    name = Column(String(100))
    professor_id = Column(Integer, ForeignKey('professors.id'))
    professor = relationship(
        "Professor",
        backref="courses"
    )
    assignments = relationship("Assignment")

    def __init__(self, course_id, course_name, professor=None):
        self.course_id = course_id
        self.name = course_name
        if professor is not None: 
            self.professor = professor

    def __repr__(self):
        return '<Course course_id=%r>' % (
            self.course_id
        )      

    @classmethod
    def get(cls, course_id):
        return cls.query.filter_by(course_id=course_id).first()

    def post_assignment(self, assignment_number, maximum_marks):
        self.assignments.append(
            Assignment(self.course_id, assignment_number, maximum_marks)
        )