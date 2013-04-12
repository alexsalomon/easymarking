from database_models import database
from database_models.transaction import commit_on_success
from database_models.assignment import Assignment
from database_models.professor import Professor
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
			return "Successfully created course '" + course_id + "'."
		else:
			return "*** Assignment number '" + str(assignment_number) + \
				"' for course '" + course_id + "' already exist."
	else:
		return "*** Course '" + course_id + "' doesn't exist."
