from database_models.handed_assignment import HandedAssignment
from engine.reports.report import Report

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
