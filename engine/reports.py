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
	try:
		report_manager = ReportManager()
		report_obj = report_manager.get_report("individual_student_feedback")
		report_obj.set_assignment(handed_assignment)
		report_obj.generate()
		print "Report for student '" + handed_assignment.student_id + \
			"' was successfully generated."
	except:
		print "*** Report for student '" + handed_assignment.student_id + \
			" could not be generated."

def generate_overall_feedback_report_for_assignment(
	course_id, 
	assignment_number
):	
	if course_id is None:
		course_id = SystemConfiguration.get_setting("working_course_id")

	if assignment_number is None:
		assignment_number = SystemConfiguration.get_setting(
			"working_assignment_number"
		)

	try:
		report_manager = ReportManager()
		report_obj = report_manager.get_report("assignment_feedback")
		report_obj.set_assignment(Assignment.get(course_id, assignment_number))
		report_obj.generate()
		print "Feedback report for assignment '" + course_id + " - A" + \
			assignment_number + "' was successfully generated."
	except:
		print "*** Feedback report for assignment '" + course_id + " - A" + \
			assignment_number + "'could not be generated."

def generate_grades_report_for_assignment(
	course_id, 
	assignment_number
):	
	if course_id is None:
		course_id = SystemConfiguration.get_setting("working_course_id")

	if assignment_number is None:
		assignment_number = SystemConfiguration.get_setting(
			"working_assignment_number"
		)

	try:
		report_manager = ReportManager()
		report_obj = report_manager.get_report("assignment_grades_txt")
		report_obj.set_assignment(Assignment.get(course_id, assignment_number))
		report_obj.generate()
		print "Grades report for assignment '" + course_id + " - A" + \
			assignment_number + "' was successfully generated."
	except:
		print "*** Grades report for assignment '" + course_id + " - A" + \
			assignment_number + "'could not be generated."

class ReportManager():
	""" ReportManager manages reports by creating a Report
		object based on the input received
	"""
	def get_report(self, report_name):
		if report_name == "individual_student_feedback":
			return StudentFeedbackReport()
		if report_name == "assignment_feedback":
			return AssignmentFeedbackReport()	
		if report_name == "assignment_grades_txt":
			return TxtAssignmentGradesReport()						

class Report():
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def generate(self):
		print "Should never hit this method"
		raise

	@abc.abstractmethod
	def get_report_file_path(self, student_id, course_id, assignment_number):
		print "Should never hit this method"
		raise

	def set_assignment(self, assignment):
		self.assignment = assignment	

	def get_assignment_path(self, course_id, assignment_number):
		project_dir = os.getcwd()
		reports_dir = project_dir+'/bin/reports/'
		course_dir = reports_dir+course_id+'/'
		assignment_dir = course_dir+'A'+str(assignment_number)+'/'
		return assignment_dir

	def open_report_file_for_write(self, file_path):
		self.create_path_if_non_existent(file_path)
		return open(file_path, 'w')

	def create_path_if_non_existent(self, file_path):
		file_dir = os.path.dirname(file_path)
		if not os.path.exists(file_dir):
			os.makedirs(file_dir)

class FeedbackReport(Report):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def generate(self):
		print "Should never hit this method"
		raise

	@abc.abstractmethod
	def get_report_file_path(self, student_id, course_id, assignment_number):
		print "Should never hit this method"
		raise

	def write_student_feedback_to_file(self, handed_assignment, report_file):	
		feedback_messages = handed_assignment.feedback_messages

		for feedback in feedback_messages:
			report_file.write(
				"-   " + feedback.message + " [-" + \
				str(feedback.marks_to_deduct) + "]\n"
			)	

		if len(feedback_messages) == 0:
			report_file.write(
				"-   " + "Good job! Keep up the good work!" + "\n"
			)	

class AssignmentFeedbackReport(FeedbackReport):

	def __repr__(self):
		return '<AssignmentFeedbackReport assignment=%r>' % (
			self.assignment
		)

	def generate(self):
		report_file_path = self.get_report_file_path(
			self.assignment.course_id, 
			self.assignment.number
		)
		report_file = self.open_report_file_for_write(report_file_path)
		handed_assignments = HandedAssignment.get_all(
			self.assignment.course_id, 
			self.assignment.number
		)		

		self.write_file_header(self.assignment, report_file)

		for handed_assignment in handed_assignments:
			self.write_student_header_to_file(handed_assignment, report_file)
			self.write_student_feedback_to_file(handed_assignment, report_file)
			report_file.write("\n")

		report_file.close()	

	def get_report_file_path(self, course_id, assignment_number):
		assignment_dir = self.get_assignment_path(course_id, assignment_number)
		file_dir = assignment_dir+"StudentFeedbacks/"
		file_path = file_dir+'feedback.txt'
		return file_path

	def write_file_header(self, assignment, report_file):
		header = "----------------------------------- Class Feedback "
		header += "-----------------------------------\n"
		header += "Course: " + self.assignment.course_id + "\n"
		header += "Assignment: " + str(self.assignment.number) + "\n"
		header += "Total Marks: " + str(self.assignment.maximum_marks) + "\n"
		header += "--------------------------------------------------"
		header += "------------------------------------\n\n"
		report_file.write(header)

	def write_student_header_to_file(self, handed_assignment, report_file):
		header = "Student '" + handed_assignment.student_id + "' - ["
		header += str(handed_assignment.marks_achieved) + "/"
		header += str(self.assignment.maximum_marks) + "]:\n"
		header += "--------------------------------\n"
		report_file.write(header)

class StudentFeedbackReport(FeedbackReport):

	def __repr__(self):
		return '<StudentFeedbackReport handed_assignment=%r>' % (
			self.handed_assignment
		)

	def set_assignment(self, handed_assignment):
		self.handed_assignment = handed_assignment

	def generate(self):
		report_file_path = self.get_report_file_path(
			self.handed_assignment.student_id, 
			self.handed_assignment.course_id, 
			self.handed_assignment.assignment_number
		)
		report_file = self.open_report_file_for_write(report_file_path)

		self.add_initial_student_feedback_message_to_file(report_file)
		self.write_student_feedback_to_file(self.handed_assignment, report_file)	
		report_file.close()	

	def get_report_file_path(self, student_id, course_id, assignment_number):
		assignment_dir = self.get_assignment_path(
			course_id,
			assignment_number
		)
		file_path = assignment_dir+student_id+'.txt'
		return file_path

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

class TxtAssignmentGradesReport(Report):

	def __repr__(self):
		return '<TxtGradesReport assignment=%r>' % (
			self.assignment
		)

	def generate(self):
		report_file_path = self.get_report_file_path(
			self.assignment.course_id, 
			self.assignment.number
		)
		report_file = self.open_report_file_for_write(report_file_path)
		handed_assignments = HandedAssignment.get_all(
			self.assignment.course_id, 
			self.assignment.number
		)		

		self.write_file_header(self.assignment, report_file)

		for handed_assignment in handed_assignments:
			self.write_student_header_to_file(handed_assignment, report_file)

		report_file.close()	

	def get_report_file_path(self, course_id, assignment_number):
		assignment_dir = self.get_assignment_path(course_id, assignment_number)
		file_dir = assignment_dir+'Grades/'
		file_path = file_dir+'A'+str(self.assignment.number)+'_grades.txt'
		return file_path

	def write_file_header(self, assignment, report_file):
		header = "------------------------------------ Class Grades "
		header += "------------------------------------\n"
		header += "Course: " + self.assignment.course_id + "\n"
		header += "Assignment: " + str(self.assignment.number) + "\n"
		header += "Total Marks: " + str(self.assignment.maximum_marks) + "\n"
		header += "--------------------------------------------------"
		header += "------------------------------------\n\n"
		header += "Student Name\t|\tGrade\n"
		header += "-------------------------------\n"
		report_file.write(header)

	def write_student_header_to_file(self, handed_assignment, report_file):
		if len(handed_assignment.student_id) > 7:
			number_of_tabs = "\t"
		else:
			number_of_tabs = "\t\t"

		header = handed_assignment.student_id + number_of_tabs + "|\t" + \
			str(handed_assignment.marks_achieved) + "\n"
		report_file.write(header)

