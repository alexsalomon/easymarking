import database
from sqlalchemy import Column, Table, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from database_models.course import Course

enrolled = Table(
    'enrolled', 
    database.Base.metadata,
    Column('student_id', String(20), ForeignKey('students.student_id')),
    Column('course_id', String(20), ForeignKey('courses.course_id'))
)

class Student(database.Base):
    __tablename__ = 'students'

    student_id = Column(String(20), primary_key=True)
    email = Column(String(254)) #TODO: figure out if this value is nullable
    courses = relationship(
        "Course",
        secondary=enrolled,
        backref="students"
    )    
    handed_assignments = relationship("HandedAssignments")

    def __init__(self, student_id, email=None):
        self.student_id = student_id
        self.email = email

    def __repr__(self):
        return '<Student student_id=%r email=%r>' % (
            self.student_id,
            self.email
        )      
