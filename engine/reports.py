import os
from database_models import database
from database_models.feedback_message import FeedbackMessage
from database_models.assignment import Assignment
from database_models.student import Student

def generate_individual_student_report(
	student_id, 
	assignment_course, 
	assignment_number
):
	try:
		file_path = create_file_path(
			student_id, 
			assignment_course, 
			assignment_number
		)
		report_file = open(file_path, 'w')	

		assignment = Assignment.query.filter_by(
			student_school_id=student_id,
			course=assignment_course,
			number=assignment_number
		).first()

		insert_marks_achieved_to_assignment_based_on_feedback_messages(assignment)
		add_initial_student_feedback_message_to_file(report_file, assignment)
		write_student_feedback_information_to_file(report_file, assignment)	
		report_file.close()
		print "Report for student '" + student_id + "' was successfully generated"
	except:
		print "*** Report could not be generated"

def get_file_path(student_id, assignment_course, assignment_number):
	project_dir = os.getcwd()
	reports_dir = project_dir+'/bin/reports/'
	student_dir = reports_dir+student_id+'/'
	course_dir = student_dir+assignment_course+'/'
	file_path = course_dir+'A'+str(assignment_number)+'_feedback.txt'
	return file_path

def create_file_path(student_id, assignment_course, assignment_number):
	file_path = get_file_path(student_id, assignment_course, assignment_number)
	file_dir = (file_path.rsplit('/', 1))[0]
	create_folders_if_non_existent(file_dir)
	return file_path

def create_folders_if_non_existent(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

def add_initial_student_feedback_message_to_file(report_file, assignment):
	report_file.write(
		"Hi,\n\nYour mark for " + assignment.course + " Assignment " + \
		str(assignment.number) + " is [" + str(assignment.marks_achieved) + \
		"/" + str(assignment.maximum_marks) + "]" + "\n\nFeedback:\n"
	)

def write_student_feedback_information_to_file(report_file, assignment):	
	feedback_messages = assignment.feedback_messages

	for feedback in feedback_messages:
		report_file.write(
			"-   " + feedback.message + " [-" + str(feedback.grade_value) + "]\n"
		)

def insert_marks_achieved_to_assignment_based_on_feedback_messages(assignment):
	marks_to_deduct = calculate_marks_deducted_for_student_assignment(assignment)
	assignment.marks_achieved = assignment.maximum_marks - marks_to_deduct


def calculate_marks_deducted_for_student_assignment(assignment):
	mark_sum = 0

	for message in assignment.feedback_messages:
		mark_sum += message.grade_value

	return mark_sum

