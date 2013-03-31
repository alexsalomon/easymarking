import database
from sqlalchemy import Column, Table, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database_models.course import Course

enrolled = Table(
	'enrolled', 
	database.Base.metadata,
    Column('student_id', String(20), ForeignKey('students.school_id')),
    Column('course_id', String(20), ForeignKey('courses.course_id'))
)

class Student(database.Base):
    __tablename__ = 'students'

    school_id = Column(String(20), primary_key=True)
    courses = relationship(
        "Course",
        secondary=enrolled
    )    

    def __init__(self, school_id):
        self.school_id = school_id

    def __repr__(self):
        return '<Student school_id=%r>' % (
            self.school_id
        )      
