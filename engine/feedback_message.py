from database_models import database
from database_models.transaction import commit_on_success
from database_models.student import Student
from database_models.feedback import Feedback
from database_models.feedback_message import FeedbackMessage, FBMessageAlias

@commit_on_success
def save_message(alias, sentence, marks_allocated):
	"Stores the feedback message to the database"
	db_session = database.session

	if not FBMessageAlias.query.get(alias):
		feedback_message = FeedbackMessage(sentence, marks_allocated)
		feedback_message.aliases.append(FBMessageAlias(alias))
		db_session.add(feedback_message)
		return "Message saved successfully under the alias '" + alias + "'."
	else:
		return "*** This alias is already representing another message."

@commit_on_success
def append_feedback(school_id, alias):
	"Uses a pre-defined feedback message to provide feedback to a student"
	db_session = database.session

	__create_student_if_doesnt_already_exist(school_id)

	alias = FBMessageAlias.query.get(alias)
	student = Student.query.filter_by(school_id=school_id).first()

	if alias and student:
		feedback = Feedback(student.id, alias.message_id)
		db_session.add(feedback)
		return "Feedback message successfully appended."
	else:
		return "*** Alias doesn't exist. Use the newfbmsg command to " \
			"create a feedback message."

def __create_student_if_doesnt_already_exist(school_id):
	db_session = database.session

	if Student.query.filter_by(school_id=school_id).first() is None:
		db_session.add( Student(school_id) )
		db_session.flush()