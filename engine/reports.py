import os, abc
from database_models import database
from database_models.feedback_message import FeedbackMessage
from database_models.assignment import Assignment
from database_models.student import Student

def generate_individual_student_feedback_report(
	student_id, 
	course_id, 
	assignment_number
):
	try:
		assignment = Assignment.query.filter_by(
			student_id=student_id,
			course_id=course_id,
			number=assignment_number
		).first()

		report_manager = ReportManager()
		report_obj = report_manager.get_report("individual_student_feedback")
		report_obj.set_assignment(assignment)
		report_obj.generate()
		print "Report for student '" + student_id + "' was successfully generated"
	except:
		print "*** Report could not be generated"

class ReportManager():
	""" ReportManager manages reports by creating a Report
		object based on the input received
	"""
	def get_report(self, report_name):
		if report_name == "individual_student_feedback":
			return StudentFeedbackReport()

class Report():
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def generate(self):
		"""Generates the report"""
		print "Should never hit this method"
		return

class StudentFeedbackReport():

	def __repr__(self):
		return '<StudentFeedbackReport assignment=%r>' % (
			self.assignment
		)

	def set_assignment(self, assignment):
		self.assignment = assignment

	def generate(self):
		file_path = self.create_file_path(
			self.assignment.student_id, 
			self.assignment.course_id, 
			self.assignment.number
		)
		report_file = open(file_path, 'w')	

		self.insert_marks_achieved_to_assignment_based_on_feedback_messages()
		self.add_initial_student_feedback_message_to_file(report_file)
		self.write_student_feedback_information_to_file(report_file)	
		report_file.close()	

	def create_file_path(self, student_id, course_id, assignment_number):
		file_path = self.get_file_path(student_id, course_id, assignment_number)
		file_dir = (file_path.rsplit('/', 1))[0]
		self.create_folders_if_non_existent(file_dir)
		return file_path

	def get_file_path(self, student_id, course_id, assignment_number):
		project_dir = os.getcwd()
		reports_dir = project_dir+'/bin/reports/'
		student_dir = reports_dir+student_id+'/'
		course_dir = student_dir+course_id+'/'
		file_path = course_dir+'A'+str(assignment_number)+'_feedback.txt'
		return file_path

	def create_folders_if_non_existent(self, directory):
		if not os.path.exists(directory):
			os.makedirs(directory)

	def add_initial_student_feedback_message_to_file(self, report_file):
		report_file.write(
			"Hi,\n\nYour mark for " + self.assignment.course_id + " Assignment " + \
			str(self.assignment.number) + " is [" + str(self.assignment.marks_achieved) + \
			"/" + str(self.assignment.maximum_marks) + "]" + "\n\nFeedback:\n"
		)

	def write_student_feedback_information_to_file(self, report_file):	
		feedback_messages = self.assignment.feedback_messages

		for feedback in feedback_messages:
			report_file.write(
				"-   " + feedback.message + " [-" + str(feedback.grade_value) + "]\n"
			)

	def insert_marks_achieved_to_assignment_based_on_feedback_messages(self):
		marks_to_deduct = self.calculate_marks_deducted_for_student_assignment()
		self.assignment.marks_achieved = self.assignment.maximum_marks - marks_to_deduct


	def calculate_marks_deducted_for_student_assignment(self):
		mark_sum = 0

		for message in self.assignment.feedback_messages:
			mark_sum += message.grade_value

		return mark_sum			

