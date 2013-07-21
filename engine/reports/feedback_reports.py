import abc

from database_models.handed_assignment import HandedAssignment
from database_models.assignment import Assignment
from engine.reports.report import Report


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
			# string = (feedback.message).replace(u'\xa0', u' ')
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