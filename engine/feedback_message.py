from database_models import database
from database_models.transaction import commit_on_success
from database_models.student import Student
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
def append_feedback(alias, school_id):
	"Uses a pre-defined feedback message to provide feedback to a student"
	db_session = database.session

	# __create_student_if_doesnt_already_exist(school_id)

	# alias = FBMessageAlias.query.get(alias)
	# feedback_message = FeedbackMessage.query.get(alias.message_id)
	# assignment = Assignment.query.get("COMP 4350", 1).first()

	# if alias and student:
	# 	db_session.add( assignment.append(feedback_message) )
	# 	return "Feedback message successfully appended."
	# else:
	# 	return "*** Alias doesn't exist. Use the newfbmsg command to " \
	# 		"create a feedback message."
	return "Needs to implement"

def __create_student_if_doesnt_already_exist(school_id):
	db_session = database.session

	if Student.query.filter_by(school_id=school_id).first() is None:
		student = Student(school_id)
		student.assignments.append(Assignment("COMP 4350", 1))	
		db_session.add( student )
		db_session.flush()