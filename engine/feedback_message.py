import os, os.path
from database_models import database
from database_models.transaction import commit_on_success
from database_models.course import Course
from database_models.student import Student
from database_models.assignment import Assignment
from database_models.handed_assignment import HandedAssignment
from database_models.system_configuration import SystemConfiguration
from database_models.feedback_message import FeedbackMessage, FBMessageAlias

@commit_on_success
def save_message(alias, message, marks_to_deduct):
	"Stores the feedback message in the database"
	result_string = ""

	if not FeedbackMessage.contains(alias):
		feedback_message = FeedbackMessage(
			alias, 
			message, 
			marks_to_deduct
		)
		result_string = "Message was saved successfully under the alias '" + \
			alias + "'."
	else:
		result_string = "*** This alias is already representing " + \
			"another message."

	return result_string

@commit_on_success
def append_feedback(alias, student_id):
	"Uses a pre-defined feedback message to provide feedback to a student"
	result_string = ""

	student_id = get_student_id_from_curr_dir_if_not_prev_specified(student_id)
	feedback_message = FeedbackMessage.get(alias)
	handed_assignment = HandedAssignment.get(
		student_id,
		SystemConfiguration.get_setting("working_course_id"),
		SystemConfiguration.get_setting("working_assignment_number")
	)	

	if not has_feedback_message_being_previously_appended(feedback_message, handed_assignment):
		handed_assignment.append_feedback_message(feedback_message)
		result_string = "Feedback message successfully appended."
	else:
		result_string = "*** Alias doesn't exist. Use the newfbmsg " \
			"command to create a feedback message."

	return result_string

def get_student_id_from_curr_dir_if_not_prev_specified(student_id):
	if student_id is None:
		student_id = os.path.basename(os.getcwd())	
	return student_id

def has_feedback_message_being_previously_appended(
	feedback_message, 
	handed_assignment
):
	previously_appended = False
	if feedback_message in handed_assignment.feedback_messages:
		previously_appended = True
	return previously_appended


