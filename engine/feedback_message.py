from database_models import database
from database_models.transaction import commit_on_success
from database_models.course import Course
from database_models.student import Student
from database_models.assignment import Assignment
from database_models.feedback_message import FeedbackMessage, FBMessageAlias

@commit_on_success
def save_message(alias, message, marks_to_deduct):
	"Stores the feedback message in the database"
	db_session = database.session

	if not FBMessageAlias.query.get(alias):
		feedback_message = FeedbackMessage(
			FBMessageAlias(alias), 
			message, 
			marks_to_deduct
		)
		return "Message saved successfully under the alias '" + alias + "'."
	else:
		return "*** This alias is already representing another message."

@commit_on_success
def append_feedback(
	alias, 
	student_id, 
	course_id, 
	assignment_number, 
	maximum_marks
):
	"Uses a pre-defined feedback message to provide feedback to a student"
	db_session = database.session

	_create_student_if_doesnt_already_exist(student_id)
	_create_course_to_existing_student_if_not_previoulsy_created(student_id, course_id)
	assignment =  _create_assignment_to_existing_student_if_not_previoulsy_created(
		student_id,
		course_id, 
		assignment_number,
		maximum_marks
	)

	feedback_message = FeedbackMessage.query.join(
		FBMessageAlias
	).filter_by(
		alias=alias
	).first()

	if feedback_message is not None and feedback_message not in assignment.feedback_messages:
		assignment.feedback_messages.append(feedback_message)
		return "Feedback message successfully appended."
	else:
		return "*** Alias doesn't exist. Use the newfbmsg command to " \
			"create a feedback message."

def _create_student_if_doesnt_already_exist(student_id):
	db_session = database.session
	student = Student.query.filter_by(student_id=student_id).first()

	if student is None:
		student = Student(student_id)
		db_session.add(student)
		db_session.flush()

	return student

def _create_course_to_existing_student_if_not_previoulsy_created(
	student_id,
	course_id
):
	db_session = database.session
	course = Course.query.filter_by(course_id=course_id).first()

	if course is None:
		student = Student.query.filter_by(student_id=student_id).first()
		course = Course(course_id, "COURSE NAME HARDCODED")
		student.courses.append(course)	
		db_session.add( student )
		db_session.flush()

	return course	

def _create_assignment_to_existing_student_if_not_previoulsy_created(
	student_id,
	course_id, 
	assignment_number,
	maximum_marks
):
	db_session = database.session
	assignment = Assignment.query.filter_by(
		student_id=student_id,
		course_id=course_id,
		number=assignment_number
	).first()

	if assignment is None:
		course = Course.query.filter_by(course_id=course_id).first()
		assignment = Assignment(
			student_id,
			course_id,
			assignment_number,
			maximum_marks
		)
		course.assignments.append(assignment)	
		db_session.add( course )
		db_session.flush()

	return assignment
