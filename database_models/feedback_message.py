from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, backref
import database

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
        return '<FeedbackMessage %r %r %r>' % (
            self.message,
            self.grade_value,   
            self.aliases
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