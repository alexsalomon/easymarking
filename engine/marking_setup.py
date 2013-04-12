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
def initiate_marking(course_id, assignment_number, email_domain):
	result_string = ""

	curr_directory = os.getcwd()
	subdirectory_names = get_immediate_subdirectories(curr_directory)	
	result_string += add_students_based_on_subdirectory_name_if_needed(subdirectory_names, email_domain)
	result_string += enrol_students_on_course_if_needed(subdirectory_names, course_id)
	result_string += create_handed_assignment_for_each_student(subdirectory_names, course_id, assignment_number)

	return result_string

def get_immediate_subdirectories(dir):
    return [filename for filename in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, filename))]

def add_students_based_on_subdirectory_name_if_needed(subdirectory_names, email_domain):
	students_created = []
	result_string = ""

	for dirname in subdirectory_names:
		if not Student.contains(dirname):
			Student(dirname, dirname+"@"+email_domain)
			students_created.append(dirname)
			result_string += "Student '" + student_id + "' " + \
				"was successfully created.\n"

	if len(subdirectory_names) == 0:
		result_string += "*** There are no subdirectories on the path '" + \
			curr_directory + "'.\n"
	elif len(students_created) == 0:
		result_string += "*** Did not need to create students for any of " + \
			"the subdirectory names since they already exist.\n"
	elif len(students_created) > 1:
		result_string += "Created a total of " + \
			str(len(students_created)) + " students.\n"			

	return result_string

def enrol_students_on_course_if_needed(subdirectory_names, course_id):
	result_string = ""

	for student_id in subdirectory_names:
		if not Student.is_enrolled(student_id, course_id):
			Student.enroll(student_id, course_id)
			result_string += "Successfully enrolled student '" + student_id + \
				"' in the course '" + course_id + "'.\n"

	return result_string

def create_handed_assignment_for_each_student(subdirectory_names, course_id, assignment_number):
	result_string = ""
	handed_assignments_count = 0

	for student_id in subdirectory_names:
		if not Student.has_handed_assignment_for_course(
			student_id, 
			course_id, 
			assignment_number
		):
			Student.create_handed_assignment(
				student_id, 
				course_id, 
				assignment_number
			)
			handed_assignments_count = handed_assignments_count + 1

	result_string += "A total of '" + str(handed_assignments_count) + \
		"' students have handed in their assignment."

	return result_string	



