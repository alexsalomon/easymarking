from engine.reports.feedback_reports import StudentFeedbackReport
from engine.reports.feedback_reports import AssignmentFeedbackReport
from engine.reports.grade_reports import TxtAssignmentGradesReport

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