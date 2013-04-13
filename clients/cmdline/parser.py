import argparse

class Parser():

	@classmethod
	def get_parser(cls, command):
		parser = None

		if command == 'ccourse':
			return cls.__get_ccourse_parser()	
		elif command == 'postasgmnt':
			return cls.__get_postasgmnt_parser()
		elif command == 'initmarking':
			return cls.__get_initmarking_parser()				
		elif command == 'newfd':
			return cls.__get_newfd_parser()					
		elif command == 'fd':
			return cls.__get_fd_parser()	
		elif command == 'gensrep':
			return cls.__get_gensrep_parser()				
		elif command == 'nextdir':
			return cls.__get_nextdir_parser()	
		elif command == 'prevdir':
			return cls.__get_prevdir_parser()									
		
		return parser

	@classmethod
	def __get_ccourse_parser(cls):		
		ccourse_parser = argparse.ArgumentParser(
			add_help=False,
			prog='ccourse'
		)
		ccourse_parser.add_argument(
			'course_id',
			help="The course id that represents the course being created"
		)
		ccourse_parser.add_argument(
			'-n',
			dest='course_name',
			action='store',
			default=None,
	        help='The course name'
		)
		ccourse_parser.add_argument(
			'-p',
			dest='prof_name',
			action='store',
			default=None,
	        help='The name of the professor that is teaching the course'
		)
		ccourse_parser.add_argument(
			'-pe',
			dest='prof_email',
			action='store',
			default=None,
	        help='The email of the professor that is teaching the course'
		)

		return ccourse_parser

	@classmethod
	def __get_postasgmnt_parser(cls):		
		postasgmnt_parser = argparse.ArgumentParser(
			add_help=False,
			prog='postasgmnt'
		)
		postasgmnt_parser.add_argument(
			'course_id',
			help="The course id"
		)
		postasgmnt_parser.add_argument(
			'assignment_number',
			type=int,
			help="The assignment number"
		)
		postasgmnt_parser.add_argument(
			'maximum_marks',
			type=is_integer_or_float, 
			help="The number of marks the assignment is worth"
		)

		return postasgmnt_parser	

	@classmethod
	def __get_initmarking_parser(cls):		
		initmarking_parser = argparse.ArgumentParser(
			add_help=False,
			prog='initmarking'
		)
		initmarking_parser.add_argument(
			'course_id',
			help="Course ID"
		)
		initmarking_parser.add_argument(
			'assignment_number',
			help="Assignment number"
		)				
		initmarking_parser.add_argument(
			'email_domain',
			help="The domain name to which the student's email address resides.\n" \
				"Example: if 'cc.umanitoba.ca' is inserted, the user's email will be " \
				"'dirname@cc.umanitoba.ca', where dirname is the name of the subdirectory."
		)		

		return initmarking_parser				

	@classmethod
	def __get_newfd_parser(cls):		
		newfd_parser = argparse.ArgumentParser(
			add_help=False,
			prog='newfd'
		)
		newfd_parser.add_argument(
			'alias',
			help="The command that represents the feedback sentence"
		)
		newfd_parser.add_argument(
			'message', 
			help="The feedback sentence to be saved"
		)
		newfd_parser.add_argument(
			'mark_value', 
			type=is_integer_or_float, 
			help="The amount of marks that should be removed when " \
				"using this sentence"
		)

		return newfd_parser

	@classmethod
	def __get_fd_parser(cls):		
		fd_parser = argparse.ArgumentParser(
			add_help=False,
			prog='fd'
		)
		fd_parser.add_argument(
			'alias', 
			help="Feedback message alias"
		)

		fd_parser.add_argument(
			'-s',
			dest='student_id',
			action='store',
			default=None,
	        help="Student's school unique identifier"
		)
		
		return fd_parser	

	@classmethod
	def __get_gensrep_parser(cls):		
		gensrep_parser = argparse.ArgumentParser(
			add_help=False,
			prog='gensrep'
		)
		gensrep_parser.add_argument(
			'-c',
			dest='course_id',
			action='store',
			default=None,
	        help="The course id"
		)
		gensrep_parser.add_argument(
			'-a',
			dest='assignment_number',
			action='store',
			default=None,
			type=int,			
	        help="The assignment number"
		)

		return gensrep_parser

	@classmethod
	def __get_nextdir_parser(cls):		
		nextdir_parser = argparse.ArgumentParser(
			add_help=False,
			prog='nextdir'
		)
		
		return nextdir_parser	

	@classmethod
	def __get_prevdir_parser(cls):		
		prevdir_parser = argparse.ArgumentParser(
			add_help=False,
			prog='prevdir'
		)
		
		return prevdir_parser						

def is_integer_or_float(string):
	try:
		float(string)
		is_float = True
	except ValueError:
		is_float = False

	try:
		int(string)
	except ValueError:
		if is_float == False:
			raise

	return string	