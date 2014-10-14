from database_models.system_configuration import SystemConfiguration
from database_models.handed_assignment import HandedAssignment
from database_models.assignment import Assignment
from engine.reports.report_manager import ReportManager

def generate_all_reports(
	course_id, 
	assignment_number
):
	generate_all_individual_student_fd_reports_for_assignment(
		course_id, 
		assignment_number
	)	
	generate_overall_feedback_report_for_assignment(
		course_id, 
		assignment_number
	)
	generate_grades_report_for_assignment(course_id, assignment_number)
	generate_xls_grades_report_for_course(course_id, assignment_number)

def generate_all_individual_student_fd_reports_for_assignment(
	course_id, 
	assignment_number
):
	(course_id, assignment_number) = SystemConfiguration.get_working_course_and_assignment(
		course_id, assignment_number
	)

	handed_assignments = HandedAssignment.get_all(course_id, assignment_number)

	for handed_assignment in handed_assignments:
		_generate_individual_student_feedback_report(handed_assignment)

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
	(course_id, assignment_number) = SystemConfiguration.get_working_course_and_assignment(
		course_id, assignment_number
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
			assignment_number + "' could not be generated."

def generate_grades_report_for_assignment(course_id, assignment_number):	
	(course_id, assignment_number) = SystemConfiguration.get_working_course_and_assignment(
		course_id, assignment_number
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
			assignment_number + "' could not be generated."	

def generate_xls_grades_report_for_course(course_id, assignment_number):	
	(course_id, assignment_number) = SystemConfiguration.get_working_course_and_assignment(
		course_id, assignment_number
	)

	try:
		report_manager = ReportManager()
		report_obj = report_manager.get_report("course_grades_xls")
		report_obj.set_assignment(Assignment.get(course_id, assignment_number))
		report_obj.generate()
		print "Grades report for course '" + course_id + \
			"' was successfully generated."
	except:
		print "*** Grades report for course '" + course_id + \
			"' could not be generated."								

