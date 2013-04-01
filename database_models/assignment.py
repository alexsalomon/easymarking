import database
from sqlalchemy import Table, Column, Integer, String, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from database_models.feedback_message import FeedbackMessage

appended_feedback = Table(
    'appended_feedback', 
    database.Base.metadata,  
    Column('student_id', String(20)),
    Column('course_id', String(20)),
    Column('assignment_number', Integer),
    Column('feedback_message_id', Integer, ForeignKey('feedback_messages.id')),
    ForeignKeyConstraint(
        ['student_id', 'course_id', 'assignment_number'],
        ['assignments.student_id', 'assignments.course_id', 'assignments.number']
    )    
)

class Assignment(database.Base):
    __tablename__ = 'assignments'

    student_id = Column(
        String(20),
        ForeignKey('students.school_id', ondelete='CASCADE'),
        primary_key=True
    )
    course_id = Column(
        String(20), 
        ForeignKey('courses.course_id', ondelete='CASCADE'),
        primary_key=True
    )
    number = Column(Integer, primary_key=True)
    marks_achieved = Column(Integer)
    maximum_marks = Column(Integer, nullable=False)
    feedback_messages = relationship(
        "FeedbackMessage",
        secondary=appended_feedback
    )

    def __init__(self, student_id, course_id, number, maximum_marks):
        self.student_id = student_id
        self.course_id = course_id
        self.number = number
        self.maximum_marks = maximum_marks

    def __repr__(self):
        return '<Assignment student_id=%r course_id=%r number=%r>' % (
            self.student_id,
            self.course_id,
            self.number
        )      
