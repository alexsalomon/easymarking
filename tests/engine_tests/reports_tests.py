import nose
from  sqlalchemy.exc import StatementError
from database_models import database
from engine.reports import calculate_marks_deducted_for_student_assignment
from database_models.student import Student
from database_models.assignment import Assignment
from database_models.feedback_message import FeedbackMessage, FBMessageAlias

database.init('test_database')

def add_initial_data_to_database():
	db_session = database.session

	student1 = Student("umkonkin")
	student2 = Student("umtest")
	db_session.add(student1)
	db_session.add(student2)
	db_session.flush()

	assignment1 = Assignment("COMP 4350", 1)
	assignment2 = Assignment("COMP 4350", 2)
	student2.assignments.append(assignment1)	
	student2.assignments.append(assignment2)

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

	assignment1.feedback_messages.append(feedback_message1)
	assignment1.feedback_messages.append(feedback_message2)
	assignment2.feedback_messages.append(feedback_message3)

	db_session.commit()

@nose.with_setup(setup=database.empty_database)
def test_calculate_marks_deducted_for_student_assignment():
	add_initial_data_to_database()
	db_session = database.session

	sum = calculate_marks_deducted_for_student_assignment("umtest", "COMP 4350", 1)
	assert sum == 2.5

	sum = calculate_marks_deducted_for_student_assignment("umtest", "COMP 4350", 2)
	assert sum == 10

	sum = calculate_marks_deducted_for_student_assignment("umkonkin", "COMP 4350", 1)
	assert sum == 0
