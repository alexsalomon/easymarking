from database_models import database
from database_models.feedback_message import FeedbackMessage

db_session = database.db_session

def save_message(message):
	"Stores the feedback message to the database"
	message = FeedbackMessage(message, 0.5)
	db_session.add(message)
	db_session.commit()
	print "All done!"
