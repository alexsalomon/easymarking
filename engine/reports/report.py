import abc, os

class Report():
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def generate(self):
		print "Should never hit this method"
		raise

	@abc.abstractmethod
	def get_report_file_path(self, student_id, course_id, assignment_number):
		print "Should never hit this method"
		raise

	def set_assignment(self, assignment):
		self.assignment = assignment	

	def get_course_path(self, course_id):
		project_dir = os.getcwd()
		reports_dir = project_dir+'/bin/Reports/'
		course_dir = reports_dir+course_id+'/'
		return course_dir

	def get_assignment_path(self, course_id, assignment_number):
		course_dir = self.get_course_path(course_id)
		assignment_dir = course_dir+'A'+str(assignment_number)+'/'
		return assignment_dir		

	def open_report_file_for_write(self, file_path):
		self.create_path_if_non_existent(file_path)
		return open(file_path, 'w')

	def create_path_if_non_existent(self, file_path):
		file_dir = os.path.dirname(file_path)
		if not os.path.exists(file_dir):
			os.makedirs(file_dir)

