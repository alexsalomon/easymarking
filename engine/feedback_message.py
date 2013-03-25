from database_models import database
from database_models.transaction import commit_on_success
from database_models.feedback_message import FeedbackMessage, FBMessageAlias

db_session = database.session

@commit_on_success
def save_message(message):
	"""Stores the feedback message to the database
	   Format: alias "message #marks_allocated"
	"""
	(alias, message) = extract_alias_from_message(message)
	(message, marks_allocated) = extract_mark_value_from_message(message)
	message = message.strip()
	feedback_message = FeedbackMessage(message, marks_allocated)
	feedback_message.aliases.append(FBMessageAlias(alias))
	db_session.add(feedback_message)

	print "Message saved successfully"

def extract_alias_from_message(message):
	(alias, message) = message.split(" ", 1)
	return (alias, message)

def extract_mark_value_from_message(message):
	marks_allocated = 0
	temp = ''

	tokens = message.split("#")
	if len(tokens) > 1:
		temp = tokens[len(tokens)-1]
	if is_integer_or_float(temp):
		marks_allocated = temp.strip()
		message = tokens[0]
	
	return (message, marks_allocated)

def is_integer_or_float(string):
	is_integer = False
	is_float = False

	try:
		float(string)
		is_float = True
	except ValueError:
		is_float = False

	try:
		int(string)
		is_integer = True
	except ValueError:
		is_integer = False

	return is_integer or is_float	
