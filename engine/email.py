import os, smtplib
 
from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from email.Utils import formatdate

from database_models.system_configuration import SystemConfiguration
from database_models.handed_assignment import HandedAssignment
from database_models.assignment import Assignment
from engine.reports.report_manager import ReportManager

# def send_email_feedback_email_to_all_students_who_handed_assignments(
# 	course_id, 
# 	assignment_number
# ):
# 	(course_id, assignment_number) = SystemConfiguration.get_working_course_and_assignment(
# 		course_id, assignment_number
# 	)
# 	parent_directory_path = SystemConfiguration.get_path(
# 		"student_email_files_directory_path",
# 		course_id, 
# 		assignment_number
# 	)

# 	#for each text file there

# 	sender = SystemConfiguration.get_setting("marker_email")
# 	receiver = Course.get(course_id).professor.email
# 	template = SystemConfiguration.get_setting("student_email_template_file_path")
# 	attachment_paths = [
# 		overall_feedback_report_file_path, 
# 		txt_grades_report_file_path,
# 		xls_grades_report_file_path
# 	]
	
# 	send_email(sender, receiver, subject, template, attachment_paths)	

def send_email_to_professor_with_overall_feedback_and_grades(
	course_id, 
	assignment_number
):
	(course_id, assignment_number) = SystemConfiguration.get_working_course_and_assignment(
		course_id, assignment_number
	)
	overall_feedback_report_file_path = SystemConfiguration.get_path(
		"overall_feedback_report_file_path",
		course_id, 
		assignment_number
	)
	txt_grades_report_file_path = SystemConfiguration.get_path(
		"txt_grades_report_file_path",
		course_id, 
		assignment_number
	)
	xls_grades_report_file_path = SystemConfiguration.get_path(
		"xls_grades_report_file_path",
		course_id, 
		assignment_number
	)

	sender = SystemConfiguration.get_setting("marker_email")
	receiver = Course.get(course_id).professor.email
	template = SystemConfiguration.get_setting("email_to_prof_template_path")
	attachment_paths = [
		overall_feedback_report_file_path, 
		txt_grades_report_file_path,
		xls_grades_report_file_path
	]
	
	send_email(sender, receiver, subject, template, attachment_paths)	

def send_email(sender, receiver, template, attachment_paths):
	message = MIMEMultipart()
	fill_message_with_correct_headers(message, sender, receiver, subject)
	write_text_message_to_email(message, template)
	attach_files_to_email(message, attachment_paths)
	send(sender, receiver, message)

def fill_message_with_correct_headers(message, sender, receiver):
    message["From"] = sender
    message["To"] = receiver
    message['Date'] = formatdate(localtime=True)
 
def write_text_message_to_email(message, template):
	with open(template) as template_file:
		text = template_file.read()
	#substitute firm in the message for subject (EXAMPLE)
	#message = re.sub(r"{{\s*subject\s*}}", subject, message)
	mimetext = MIMEText(text)
	message.attach(mimetext)

def attach_files_to_email(message, attachment_paths):
	for attachment_path in attachment_paths:
		attachment = MIMEBase('application', "octet-stream")
		attachment.set_payload( open(attachment_path,"rb").read() )
		Encoders.encode_base64(attachment)
		attachment.add_header(
			'Content-Disposition', 
			'attachment; filename="%s"' % os.path.basename(attachment_path)
		)
		message.attach(attachment)
 
def send(sender, receiver, message):
	host = SystemConfiguration.get_setting("email_host")
	server = smtplib.SMTP(host)

	host_login_username = SystemConfiguration.get_setting("email_host_username")
	host_login_password = SystemConfiguration.get_setting("email_host_password")

	if host_login_password is not None and host_login_username is not None:
		server.login(username, password)

	try:
		server.sendmail(sender, receiver, message.as_string())
		server.close()
	except SMTPException, e:
		print "*** Unable to send email. Error: %s" % str(e)
