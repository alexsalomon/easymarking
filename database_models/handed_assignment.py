import database
from sqlalchemy import Table, Column, Integer, String, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from database_models.course import Course
from database_models.assignment import Assignment
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
        [
            'handed_assignments.student_id', 
            'handed_assignments.course_id', 
            'handed_assignments.assignment_number'
        ]
    )    
)

class HandedAssignment(database.Base):
    __tablename__ = 'handed_assignments'

    student_id = Column(
        String(20),
        ForeignKey('students.student_id', ondelete='CASCADE'),
        primary_key=True
    )
    course_id = Column(
        String(20), 
        ForeignKey('courses.course_id', ondelete='CASCADE'),
        primary_key=True
    )
    assignment_number = Column(
        Integer,
        ForeignKey('assignments.number', ondelete='CASCADE'),
        primary_key=True
    )    
    marks_achieved = Column(Integer)
    feedback_messages = relationship(
        "FeedbackMessage",
        secondary=appended_feedback
    )

    def __init__(self, student_id, course_id, assignment_number):
        self.student_id = student_id
        self.course_id = course_id
        self.assignment_number = assignment_number

    def __repr__(self):
        return '<Assignment student_id=%r course_id=%r assignment_number=%r>' % (
            self.student_id,
            self.course_id,
            self.assignment_number
        )      

    @classmethod
    def get(cls, student_id, course_id, assignment_number):
        return cls.query.filter_by(
            student_id=student_id,
            course_id=course_id,
            assignment_number=assignment_number
        ).first()

    @classmethod
    def get_all(cls, course_id, assignment_number):
        return cls.query.filter_by(
            course_id=course_id,
            assignment_number=assignment_number
        ).all()        

    def append_feedback_message(self, feedback_message):
        self.feedback_messages.append(feedback_message)

