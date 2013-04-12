import database
from sqlalchemy import Column, Integer, String, ForeignKey

class Assignment(database.Base):
    __tablename__ = 'assignments'

    course_id = Column(
        String(20), 
        ForeignKey('courses.course_id', ondelete='CASCADE'),
        primary_key=True
    )
    number = Column(Integer, primary_key=True)
    maximum_marks = Column(Integer, nullable=False)

    @classmethod
    def get(cls, course_id, assignment_number):
        return cls.query.filter_by(
            course_id=course_id, 
            number=assignment_number
        ).first()

    def __init__(self, course_id, number, maximum_marks):
        self.course_id = course_id
        self.number = number
        self.maximum_marks = maximum_marks

    def __repr__(self):
        return '<Assignment course_id=%r number=%r>' % (
            self.course_id,
            self.number
        )      
