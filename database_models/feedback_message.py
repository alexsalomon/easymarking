from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship, backref
from database import Base

class FeedbackMessage(Base):
    __tablename__ = 'feedback_messages'

    id = Column(Integer, primary_key=True)
    message = Column(String(500), nullable=False)
    grade_value = Column(Float)

    def __init__(self, message, grade_value):
        self.message = message
        self.grade_value = grade_value

    def __repr__(self):
        return '<FeedbackMessage %r %r>' % (
            self.message,
            self.grade_value
        )      
