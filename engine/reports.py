import os, abc
from database_models import database
from database_models.system_configuration import SystemConfiguration
from database_models.handed_assignment import HandedAssignment
from database_models.feedback_message import FeedbackMessage
from database_models.assignment import Assignment
from database_models.student import Student

def generate_all_individual_student_fd_reports_for_assignment(
	course_id, 
	assignment_number
):
	if course_id is None:
		course_id = SystemConfiguration.get_setting("working_course_id")

	if assignment_number is None:
		assignment_number = SystemConfiguration.get_setting(
			"working_assignment_number"
		)

	handed_assignments = HandedAssignment.get_all(course_id, assignment_number)

	for handed_assignment in handed_assignments:
		generate_individual_student_feedback_report(handed_assignment)

def generate_individual_student_feedback_report(handed_assignment):
	#try:
	report_manager = ReportManager()
	report_obj = report_manager.get_report("individual_student_feedback")
	report_obj.set_handed_assignment(handed_assignment)
	report_obj.generate()
	print "Report for student '" + handed_assignment.student_id + \
		"' was successfully generated."
	# except:
	# 	print "*** Report for student '" + handed_assignment.student_id + \
	# 		"could not be generated."

# def generate_assignment_feedback_report(
# 	student_id, 
# 	course_id, 
# 	assignment_number
# ):
# 	try:
# 		report_manager = ReportManager()
# 		report_obj = report_manager.get_report("assignment_feedback")
# 		report_obj.generate()
# 		print "Report for assignment '" + course_id + " - A" + \
# 			assignment_number + "' was successfully generated."
# 	except:
# 		print "*** Report could not be generated."


class ReportManager():
	""" ReportManager manages reports by creating a Report
		object based on the input received
	"""
	def get_report(self, report_name):
		if report_name == "individual_student_feedback":
			return StudentFeedbackReport()
		if report_name == "assignment_feedback":
			return AssignmentFeedbackReport()			

class Report():
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def generate(self):
		"""Generates the report"""
		print "Should never hit this method"
		return

	def set_handed_assignment(self, handed_assignment):
		self.handed_assignment = handed_assignment

class AssignmentFeedbackReport(Report):

	def __repr__(self):
		return '<AssignmentFeedbackReport assignment=%r>' % (
			self.assignment
		)

	def generate(self):
		raise "NotImplemented"
		# #Every report needs a path to be written to
		# file_path = self.create_file_path()
		# #every report needs a file handler to write
		# report_file = open(file_path, 'w')	

		# course = get_course()
		# assignments = course.assignments WHERE number = assignment_number
		# for assignment in assignments:
		# 	#write to file

		# report_file.close()	

class StudentFeedbackReport(Report):

	def __repr__(self):
		return '<StudentFeedbackReport handed_assignment=%r>' % (
			self.handed_assignment
		)

	def generate(self):
		file_path = self.create_file_path(
			self.handed_assignment.student_id, 
			self.handed_assignment.course_id, 
			self.handed_assignment.assignment_number
		)
		report_file = open(file_path, 'w')	

		self.add_initial_student_feedback_message_to_file(report_file)
		self.write_student_feedback_information_to_file(report_file)	
		report_file.close()	

	def create_file_path(self, student_id, course_id, assignment_number):
		file_path = self.get_file_path(student_id, course_id, assignment_number)
		file_dir = os.path.dirname(file_path)
		self.create_folders_if_non_existent(file_dir)
		return file_path

	def get_file_path(self, student_id, course_id, assignment_number):
		project_dir = os.getcwd()
		reports_dir = project_dir+'/bin/reports/'
		course_dir = reports_dir+course_id+'/'
		assignment_dir = course_dir+'A'+str(assignment_number)+'/'
		file_path = assignment_dir+student_id+'.txt'
		return file_path

	def create_folders_if_non_existent(self, directory):
		if not os.path.exists(directory):
			os.makedirs(directory)	

	def add_initial_student_feedback_message_to_file(self, report_file):
		assignment = Assignment.get(
			self.handed_assignment.course_id, 
			self.handed_assignment.assignment_number
		)
		report_file.write(
			"Hi,\n\nYour mark for " + assignment.course_id + " Assignment " + \
			str(assignment.number) + " is [" + str(self.handed_assignment.marks_achieved) + \
			"/" + str(assignment.maximum_marks) + "]" + "\n\nFeedback:\n"
		)

	def write_student_feedback_information_to_file(self, report_file):	
		feedback_messages = self.handed_assignment.feedback_messages

		for feedback in feedback_messages:
			report_file.write(
				"-   " + feedback.message + " [-" + str(feedback.marks_to_deduct) + "]\n"
			)	

		if len(feedback_messages) == 0:
			report_file.write(
				"-   " + "Good job! Keep up the good work!" + "\n"
			)	


