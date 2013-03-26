from database_models import database
from database_models.transaction import commit_on_success
from database_models.feedback_message import FeedbackMessage, FBMessageAlias

db_session = database.session

@commit_on_success
def save_message(alias, sentence, marks_allocated):
	"""Stores the feedback message to the database
	   Format: alias message marks_allocated
	"""
	feedback_message = FeedbackMessage(sentence, marks_allocated)
	feedback_message.aliases.append(FBMessageAlias(alias))
	db_session.add(feedback_message)
	print "Message saved successfully under the alias '" + alias + "'."
