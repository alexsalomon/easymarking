from database_models.system_configuration import SystemConfiguration
from database_models.handed_assignment import HandedAssignment
from database_models.assignment import Assignment
from engine.reports.report_manager import ReportManager

def send_email_to_professor_with_overall_feedback_and_grades(
	course_id, 
	assignment_number
):
	if course_id is None:
		course_id = SystemConfiguration.get_setting("working_course_id")

	if assignment_number is None:
		assignment_number = SystemConfiguration.get_setting(
			"working_assignment_number"
		)

	