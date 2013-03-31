import database
from sqlalchemy import Table, Column, Integer, String, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

appended_feedback = Table(
    'appended_feedback', 
    database.Base.metadata,  
    Column('student_school_id', Integer),
    Column('assignment_course', Integer),
    Column('assignment_number', Integer),
    Column('feedback_message_id', Integer, ForeignKey('feedback_messages.id')),
    ForeignKeyConstraint(
        ['student_school_id', 'assignment_course', 'assignment_number'],
        ['assignments.student_school_id', 'assignments.number', 'assignments.number']
    )    
)

class Assignment(database.Base):
    __tablename__ = 'assignments'

    student_school_id = Column(
        Integer,
        ForeignKey('students.school_id', ondelete='CASCADE'),
        primary_key=True
    )
    course = Column(String(20), primary_key=True)
    number = Column(Integer, primary_key=True)
    marks_achieved = Column(Integer)
    maximum_marks = Column(Integer, nullable=False)
    feedback_messages = relationship(
        "FeedbackMessage",
        secondary=appended_feedback
    )

    def __init__(self, course, number, maximum_marks):
        self.number = number
        self.course = course
        self.maximum_marks = maximum_marks

    def __repr__(self):
        return '<Assignment student_id=%r course=%r number=%r>' % (
            self.student_id,
            self.course,
            self.number
        )      
