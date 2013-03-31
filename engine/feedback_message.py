from database_models import database
from database_models.transaction import commit_on_success
from database_models.student import Student
from database_models.assignment import Assignment
from database_models.feedback_message import FeedbackMessage, FBMessageAlias

@commit_on_success
def save_message(alias, message, marks_allocated):
	"Stores the feedback message to the database"
	db_session = database.session

	if not FBMessageAlias.query.get(alias):
		feedback_message = FeedbackMessage(message, marks_allocated)
		feedback_message.aliases.append(FBMessageAlias(alias))
		db_session.add(feedback_message)
		return "Message saved successfully under the alias '" + alias + "'."
	else:
		return "*** This alias is already representing another message."

@commit_on_success
def append_feedback(alias, school_id, assignment_course, assignment_number):
	"Uses a pre-defined feedback message to provide feedback to a student"
	db_session = database.session

	student = _create_student_if_doesnt_already_exist(school_id)
	assignment =  _append_assignment_to_existing_student_if_he_doesnt_already_have_it(
		school_id,
		assignment_course, 
		assignment_number
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

def _create_student_if_doesnt_already_exist(school_id):
	db_session = database.session
	student = Student.query.filter_by(school_id=school_id).first()

	if student is None:
		student = Student(school_id)
		db_session.add(student)
		db_session.flush()

	return student

def _append_assignment_to_existing_student_if_he_doesnt_already_have_it(
	school_id,
	assignment_course, 
	assignment_number
):
	db_session = database.session
	assignment = Assignment.query.filter_by(
		student_school_id=school_id,
		course=assignment_course,
		number=assignment_number
	).first()

	if assignment is None:
		student = Student.query.filter_by(school_id=school_id).first()
		assignment = Assignment(assignment_course, assignment_number)
		student.assignments.append(assignment)	
		db_session.add( student )
		db_session.flush()

	return assignment
