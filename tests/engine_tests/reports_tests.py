import nose
from  sqlalchemy.exc import StatementError
from database_models import database
from engine.reports import calculate_marks_deducted_for_student_assignment
from database_models.feedback_message import FBMessageAlias, FeedbackMessage
from database_models.student import Student
from database_models.feedback import Feedback

database.init('test_database')

def add_initial_data_to_database():
	db_session = database.session

	student1 = Student("umkonkin")
	student2 = Student("umtest")
	db_session.add(student1)
	db_session.add(student2)
	db_session.flush()

	feedback_message1 = FeedbackMessage(
		"You should have been using constants in you assignment!",
		0.5
	)
	feedback_message2 = FeedbackMessage(
		"No duplications!!",
		2
	)
	feedback_message3 = FeedbackMessage(
		"UGH, where is that recursion you should have implemented?",
		10
	)	
	feedback_message1.aliases.append(FBMessageAlias("const"))
	feedback_message2.aliases.append(FBMessageAlias("dup"))
	feedback_message3.aliases.append(FBMessageAlias("rec"))
	db_session.add(feedback_message1)
	db_session.add(feedback_message2)
	db_session.add(feedback_message3)
	db_session.flush()

	feedback1 = Feedback(student2.school_id, feedback_message1.id)
	feedback2 = Feedback(student2.school_id, feedback_message2.id)
	feedback3 = Feedback(student2.school_id, feedback_message3.id)
	db_session.add(feedback1)
	db_session.add(feedback2)
	db_session.add(feedback3)

	db_session.commit()

@nose.with_setup(setup=database.empty_database)
def test_calculate_marks_deducted_for_student_assignment():
	add_initial_data_to_database()
	db_session = database.session

	sum = calculate_marks_deducted_for_student_assignment("umtest")
	assert sum == 12.5

	sum = calculate_marks_deducted_for_student_assignment("umkonkin")
	assert sum == None
