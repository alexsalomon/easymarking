import os, os.path
from database_models import database
from database_models.transaction import commit_on_success
from database_models.assignment import Assignment
from database_models.professor import Professor
from database_models.student import Student
from database_models.course import Course

@commit_on_success
def create_course(course_id, course_name=None, prof_name=None, prof_email=None):
	professor = create_or_retrieve_professor(prof_name, prof_email)
	if Course.get(course_id) is None:
		course = Course(course_id, course_name, professor)
		return "Successfully created course '" + course_id + "'."
	else:
		return "*** Course '" + course_id + "' already exists."

def create_or_retrieve_professor(prof_name, prof_email):
	db_session = database.session

	if prof_name is not None:
		professor = Professor.get(prof_name)
		if professor is None:
			professor = Professor(prof_name, prof_email)
			db_session.flush()
		return professor
	else:
		return None

@commit_on_success
def post_assignment(course_id, assignment_number, maximum_marks):
	course = Course.get(course_id)
	if course is not None:
		assignment = Assignment.get(course_id, assignment_number)
		if assignment not in course.assignments:
			course.post_assignment(assignment_number, maximum_marks)
			return "Successfully posted Assignment number '" + \
				str(assignment_number) + "' for course '" + \
				course_id + "."
		else:
			return "*** Assignment number '" + str(assignment_number) + \
				"' for course '" + course_id + "' already exist."
	else:
		return "*** Course '" + course_id + "' doesn't exist."

@commit_on_success
def create_students_from_directory_names(email_domain):
	curr_directory = os.getcwd()
	directories = get_immediate_subdirectories(curr_directory)
	students_created = []
	result_string = ""

	if len(directories) == 0:
		result_string += "*** There are no subdirectories on the path '" + \
			curr_directory + "'."
		return result_string

	for dirname in directories:
		student = Student.get(dirname)
		if student is None:
			Student(dirname, dirname+"@"+email_domain)
			students_created.append(dirname)

	for student_id in students_created:
		result_string += "Student '" + student_id + "' " + \
			"was successfully created.\n"

	if len(students_created) == 0:
		result_string += "*** Already created students for all " + \
			"the subdirectory names."
	elif len(students_created) > 1:
		result_string += "Created a total of " + \
			str(len(students_created)) + " students."			

	return result_string

def get_immediate_subdirectories(dir):
    return [filename for filename in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, filename))]


