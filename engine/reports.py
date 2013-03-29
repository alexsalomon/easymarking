from database_models import database
from database_models.feedback_message import FeedbackMessage
from database_models.assignment import Assignment
from database_models.student import Student

def calculate_marks_deducted_for_student_assignment(
	school_id,
	assignment_course, 
	assignment_number
):
	db_session = database.session

	mark_sum = 0

	student = Student.query.filter_by(school_id=school_id).first()
	if student is not None:
		assignment = Assignment.query.filter_by(
			course=assignment_course,
			number=assignment_number,
			student_id=student.id
		).first()
		if assignment is not None:
			for message in assignment.feedback_messages:
				mark_sum += message.grade_value

	else:
		mark_sum = None

	return mark_sum