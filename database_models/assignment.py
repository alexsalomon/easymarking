import database
from sqlalchemy import Table, Column, Integer, String, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

appended_feedback = Table(
    'appended_feedback', 
    database.Base.metadata,  
    Column('assignment_course', Integer),
    Column('assignment_number', Integer),
    Column('feedback_message_id', Integer, ForeignKey('feedback_messages.id')),
    ForeignKeyConstraint(
        ['assignment_course', 'assignment_number'],
        ['assignments.course', 'assignments.number']
    )    
)

class Assignment(database.Base):
    __tablename__ = 'assignments'

    course = Column(String(20), primary_key=True)
    number = Column(Integer, primary_key=True)
    student_id = Column(
        Integer,
        ForeignKey('students.id', ondelete='CASCADE')
    )
    final_grade = Column(String(3))
    feedback_messages = relationship(
        "FeedbackMessage",
        secondary=appended_feedback
    )

    def __init__(self, course, number):
        self.number = number
        self.course = course

    def __repr__(self):
        return '<Assignment course=%r number=%r student_id=%r final_grade=%r>' % (
            self.course,
            self.number,
            self.student_id,
            self.final_grade
        )      
