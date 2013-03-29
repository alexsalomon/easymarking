from database_models import database
from database_models.student import Student
from database_models.feedback import Feedback
from database_models.feedback_message import FeedbackMessage

def calculate_marks_deducted_for_student_assignment(school_id):
	db_session = database.session

	student = Student.query.filter_by(school_id=school_id).first()
	mark_sum = 0

	if student is not None:
		student_messages = Feedback.query.filter_by(student_id=school_id).all()
		print student_messages
		joined_table = db_session.query(student_messages).join(FeedbackMessage).all()

		for message in joined_table:
			mark_sum += message.grade_value

	else:
		mark_sum = None

	return mark_sum