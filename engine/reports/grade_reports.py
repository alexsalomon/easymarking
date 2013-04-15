from xlwt import Workbook, easyxf

from database_models.handed_assignment import HandedAssignment
from database_models.course import Course
from engine.reports.report import Report

class TxtAssignmentGradesReport(Report):

	def __repr__(self):
		return '<TxtAssignmentGradesReport assignment=%r>' % (
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

class XlsCourseGradesReport(Report):

	student_id_column = 0
	first_assignment_column = 1

	def __repr__(self):
		return '<XlsCourseGradesReport assignment=%r>' % (
			self.assignment
		)

	def generate(self):
		report_file_path = self.get_report_file_path(
			self.assignment.course_id
		)		

		course = Course.get(self.assignment.course_id)

		book = Workbook()
		sheet = book.add_sheet(course.course_id)
		student_count = 1

		self.write_column_titles_to_xls(sheet, course)

		for student in course.students:
			row = sheet.row(student_count)
			self.write_student_id_to_xls(row, student)
			self.write_student_grades_to_xls(row, student, course)
			student_count += 1

		book.save(report_file_path)

	def get_report_file_path(self, course_id):
		course_dir = self.get_course_path(course_id)
		file_path = course_dir+'grades.xls'
		return file_path

	def write_column_titles_to_xls(self, sheet, course):
		format = easyxf(
 			'font: name Calibri, bold on, height 240;'
 			'align: vertical center, horizontal center;'
 		)		
		sheet.write(0, self.student_id_column, 'Student ID', format)
		column = self.first_assignment_column

		for assignment in course.assignments:
			sheet.write(0, column, 'A'+str(assignment.number), format)
			column += 1

	def write_student_id_to_xls(self, row, student):
		student_id = student.student_id
		format = easyxf(
 			'font: name Calibri, height 240;'
 			'align: vertical center, horizontal center;'
 		)			
		row.write(self.student_id_column, student_id, format)

	def write_student_grades_to_xls(self, row, student, course):
		format = easyxf(
 			'font: name Calibri, height 240;'
 			'align: vertical center, horizontal center;'
 		)	
		column = self.first_assignment_column

		for assignment in course.assignments:
			handed_assignment = HandedAssignment.get(
				student.student_id,
				course.course_id,
				assignment.number
			)
			row.write(column, handed_assignment.marks_achieved, format)
			column += 1



