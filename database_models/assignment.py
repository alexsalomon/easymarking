import database
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database_models.feedback_message import appended_feedback

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

    def __init__(self, number, course):
        self.number = number
        self.course = course

    def __repr__(self):
        return '<Assignment course=%r number=%r student_id=%r final_grade=%r>' % (
            self.course,
            self.number,
            self.student_id,
            self.final_grade
        )      
