import nose
from  sqlalchemy.exc import StatementError
from database_models import database
from engine.feedback_message import save_message
from database_models.feedback_message import FBMessageAlias, FeedbackMessage

database.init('test_database')

@nose.with_setup(setup=database.empty_database)
def test_save_message_multiple_times_successeds():
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
		assert success_message in (save_message(
			aliases_to_add[index],
			messages_to_add[index],
			marks_to_add[index]
		))

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

