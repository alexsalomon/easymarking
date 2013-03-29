from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
import database

appended_feedback = Table(
    'appended_feedback', 
    database.Base.metadata,    
    Column('assignment_course', Integer, ForeignKey('assignments.course')),
    Column('assignment_number', Integer, ForeignKey('assignments.number')),
    Column('feedback_message_id', Integer, ForeignKey('feedback_messages.id'))
)

class FeedbackMessage(database.Base):
    __tablename__ = 'feedback_messages'

    id = Column(Integer, primary_key=True)
    message = Column(String(500), nullable=False)
    grade_value = Column(Float)
    aliases = relationship("FBMessageAlias")

    def __init__(self, message, grade_value):
        self.message = message
        self.grade_value = grade_value

    def __repr__(self):
        return '<FeedbackMessage %r %r>' % (
            self.message,
            self.grade_value
        )      

class FBMessageAlias(database.Base):
    __tablename__ = 'fb_message_aliases'

    alias = Column(String(50), primary_key=True)
    message_id = Column(
        Integer,
        ForeignKey('feedback_messages.id', ondelete='CASCADE')
    )

    def __init__(self, alias):
        self.alias = alias

    def __repr__(self):
        return '<FBMessageAlias message_id=%r, alias=%r>' % (
            self.message_id,
            self.alias
        )   