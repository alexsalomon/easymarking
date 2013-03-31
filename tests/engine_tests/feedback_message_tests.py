import nose
from  sqlalchemy.exc import StatementError
from database_models import database
from engine.feedback_message import save_message, append_feedback
from engine.feedback_message import _create_student_if_doesnt_already_exist
from engine.feedback_message import _append_assignment_to_existing_student_if_he_doesnt_already_have_it
from database_models.feedback_message import FBMessageAlias, FeedbackMessage
from database_models.student import Student
from database_models.assignment import Assignment
from database_models.transaction import commit_on_success

database.init('test_database')

def add_initial_data_to_database():
	db_session = database.session

	student1 = Student("umkonkin")
	student2 = Student("umtest")
	db_session.add(student1)
	db_session.add(student2)
	db_session.commit()

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
	db_session.commit()

@nose.with_setup(setup=database.empty_database)
def test_save_message_multiple_times_succeeds():
	success_message = "Message saved successfully under the alias"
	aliases_to_add = (
		'alias', 
		'alias2', 
		'alias3', 
		'alias4', 
		'alias5', 
		'alias6', 
		'alias7', 
		'alias8', 
		'alias9'
	)
	messages_to_add = (
		'short message',
		'message',
		'long long long message, coma. ":.>,<-=+-00982``}|}{]=',
		'<>,./?~`!@#$%^&*()_+|}{[]\=-0987654321qjIjsa//,.\'\'\'',
		'just another message',
		'Me and "you". yeah, that\'s right "you"',
		'A reasonable message',
		'A reasonable message A reasonable message A reasonable message A reasonable message A reasonable message A reasonable message A reasonable message A reasonable message A reasonable message',
		''
	)
	marks_to_add = (
		0,
		0.0,
		0.1,
		10,
		100000000000000,
		-123,
		-0,
		-0.1,
		-100000000000000
	)

	for index in range(0, len(aliases_to_add)):
		assert success_message in (
			save_message(
				aliases_to_add[index],
				messages_to_add[index],
				marks_to_add[index]
			)
		)

	index = 0
	aliases = database.session.query(FBMessageAlias.alias).all()
	for alias in aliases:
		assert alias.alias == aliases_to_add[index]
		index = index+1

	index = 0
	messages = database.session.query(FeedbackMessage).all()
	assert len(messages) == 9
	for message in messages:
		assert message.message == messages_to_add[index]
		assert message.grade_value == marks_to_add[index]
		assert message.aliases[0].alias == aliases_to_add[index]
		index = index+1


@nose.with_setup(setup=database.empty_database)
def test_save_message_with_existing_alias_doesnt_complete_transaction():
	success_message = "Message saved successfully under the alias"
	failure_message = "*** This alias is already representing another message."

	assert success_message in (save_message('alias', 'message', 1))
	aliases_before_attempt = database.session.query(FBMessageAlias.alias).all()
	messages_before_attempt = database.session.query(FeedbackMessage).all()

	assert failure_message in (save_message('alias', 'message', 1))
	aliases_after_attempt = database.session.query(FBMessageAlias.alias).all()
	messages_after_attempt = database.session.query(FeedbackMessage).all()
	
	assert aliases_before_attempt == aliases_after_attempt
	assert messages_before_attempt == messages_after_attempt

@nose.tools.raises(StatementError)
@nose.with_setup(setup=database.empty_database)
def test_save_message_with_non_float_or_integer_marks_allocated_throws_exception():
	save_message('alias', 'message', 'muhahaha')

@nose.with_setup(setup=database.empty_database)
def test__create_student_if_doesnt_already_exist_with_non_existent_student():
	assert None is Student.query.filter_by(school_id="umtest1").first()
	student = _create_student_if_doesnt_already_exist("umtest1")
	assert student == Student.query.filter_by(school_id="umtest1").first()

	assert None is Student.query.filter_by(school_id="umtest2").first()
	student = _create_student_if_doesnt_already_exist("umtest2")
	assert student == Student.query.filter_by(school_id="umtest2").first()

	assert None is Student.query.filter_by(school_id="umtest3").first()
	student = _create_student_if_doesnt_already_exist("umtest3")
	assert student == Student.query.filter_by(school_id="umtest3").first()		

	assert Student.query.count() == 3

@nose.with_setup(setup=database.empty_database)
def test__create_student_if_doesnt_already_exist_with_existent_student():	
	student_expected = create_student("umtest1")
	assert student_expected == Student.query.filter_by(school_id="umtest1").first()
	
	student = _create_student_if_doesnt_already_exist("umtest1")
	assert student == student_expected

	student = _create_student_if_doesnt_already_exist("umtest1")
	assert student == student_expected	

	assert Student.query.count() == 1

@nose.with_setup(setup=database.empty_database)
def test__append_assignment_to_existing_student_if_he_doesnt_already_have_it():
	#create student and check if student exists
	student = create_student("umtest1")
	assert student == Student.query.filter_by(school_id="umtest1").first()
	
	assert None is query_assignment("umtest1", "1010", 1)
	assignment = _append_assignment_to_existing_student_if_he_doesnt_already_have_it(
		"umtest1",
		"1010",
		1
	)
	assert assignment == query_assignment("umtest1", "1010", 1)

	assert None is query_assignment("umtest1", "1010", 2)
	assignment = _append_assignment_to_existing_student_if_he_doesnt_already_have_it(
		"umtest1",
		"1010",
		2
	)
	assert assignment == query_assignment("umtest1", "1010", 2)

	assert None is query_assignment("umtest1", "COMP1020", 1)
	assignment = _append_assignment_to_existing_student_if_he_doesnt_already_have_it(
		"umtest1",
		"COMP1020",
		1
	)
	assert assignment == query_assignment("umtest1", "COMP1020", 1)	

	assert Assignment.query.count() == 3

@nose.tools.raises(AttributeError)
@nose.with_setup(setup=database.empty_database)
def test__append_assignment_to_NON_existing_student_raises_exception():
	assert None is Student.query.filter_by(school_id="umtest1").first()
	assert None is query_assignment("umtest1", "1010", 1)
	_append_assignment_to_existing_student_if_he_doesnt_already_have_it(
		"umtest1",
		"1010",
		1
	)

@nose.with_setup(setup=database.empty_database)
def test_append_feedback_with_existing_data():
	add_initial_data_to_database()
	success_message = "Feedback message successfully appended."
	failure_message = "*** Alias doesn't exist. Use the newfbmsg " \
		"command to create a feedback message."

	assignment1 = query_assignment("umtest", "COMP 4350", 1)
	assignment2 = query_assignment("umtest", "COMP 4350", 2)
	assert len(assignment1.feedback_messages) == 0	
	assert len(assignment2.feedback_messages) == 0

	assert success_message == append_feedback("const", "umtest", "COMP 4350", 1)
	assert len(assignment1.feedback_messages) == 1
	assert (assignment1.feedback_messages)[0].message == "You should have been using constants in you assignment!"

	assert success_message == append_feedback("const", "umtest", "COMP 4350", 2)
	assert len(assignment2.feedback_messages) == 1
	assert (assignment2.feedback_messages)[0].message == "You should have been using constants in you assignment!"

	assert success_message == append_feedback("rec", "umtest", "COMP 4350", 1)
	assert len(assignment1.feedback_messages) == 2

	assert success_message == append_feedback("dup", "umtest", "COMP 4350", 1)
	assert len(assignment1.feedback_messages) == 3	

	assert failure_message == append_feedback("rec", "umtest", "COMP 4350", 1)
	assert len(assignment1.feedback_messages) == 3

	assert failure_message == append_feedback("dup", "umtest", "COMP 4350", 1)
	assert len(assignment1.feedback_messages) == 3		

@nose.with_setup(setup=database.empty_database)
def test_append_feedback_creating_new_student_and_assignment():
	add_initial_data_to_database()
	success_message = "Feedback message successfully appended."
	failure_message = "*** Alias doesn't exist. Use the newfbmsg " \
		"command to create a feedback message."
	
	assert None is Student.query.get("umnull")
	assert None is query_assignment("umnull", "COMP 4350", 1)

	assert success_message == append_feedback("const", "umnull", "COMP 4350", 1)
	assert None is not Student.query.get("umnull")
	assignment = query_assignment("umnull", "COMP 4350", 1)
	assert None is not assignment
	assert len(assignment.feedback_messages) == 1
	assert (assignment.feedback_messages)[0].message == "You should have been using constants in you assignment!"

	assert failure_message == append_feedback("const", "umnull", "COMP 4350", 1)
	assert len(assignment.feedback_messages) == 1
	assert (assignment.feedback_messages)[0].message == "You should have been using constants in you assignment!"

@nose.with_setup(setup=database.empty_database)
def test_append_feedback_creating_new_assignment():
	add_initial_data_to_database()
	success_message = "Feedback message successfully appended."
	failure_message = "*** Alias doesn't exist. Use the newfbmsg " \
		"command to create a feedback message."
	
	assert None is not Student.query.get("umtest")
	assert None is query_assignment("umtest", "COMP1010", 1)

	assert success_message == append_feedback("const", "umtest", "COMP1010", 1)
	assignment = query_assignment("umtest", "COMP1010", 1)
	assert None is not assignment
	assert len(assignment.feedback_messages) == 1
	assert (assignment.feedback_messages)[0].message == "You should have been using constants in you assignment!"

	assert failure_message == append_feedback("const", "umtest", "COMP1010", 1)
	assert len(assignment.feedback_messages) == 1
	assert (assignment.feedback_messages)[0].message == "You should have been using constants in you assignment!"

@nose.with_setup(setup=database.empty_database)
def test_append_feedback_with_bogus_alias():	
	add_initial_data_to_database()
	success_message = "Feedback message successfully appended."
	failure_message = "*** Alias doesn't exist. Use the newfbmsg " \
		"command to create a feedback message."

	assignment = query_assignment("umtest", "COMP 4350", 1)

	assert None is not Student.query.get("umtest")
	assert None is not assignment

	assert len(assignment.feedback_messages) == 0
	assert failure_message == append_feedback("bogus", "umtest", "COMP 4350", 1)
	assert len(assignment.feedback_messages) == 0

	assert len(assignment.feedback_messages) == 0
	assert failure_message == append_feedback("bogubogu", "umtest", "COMP 4350", 1)
	assert len(assignment.feedback_messages) == 0

	assert len(assignment.feedback_messages) == 0
	assert failure_message == append_feedback(100, "umtest", "COMP 4350", 1)
	assert len(assignment.feedback_messages) == 0		

def query_assignment(school_id, assignment_course, assignment_number):
	return Assignment.query.filter_by(
		student_school_id=school_id,
		course=assignment_course,
		number=assignment_number
	).first()	

def create_student(school_id):
	db_session = database.session
	student = Student(school_id)
	db_session.add(student)
	db_session.commit()
	return student
