import argparse

class Parser():

	@classmethod
	def get_parser(cls, command):
		parser = None

		if command == 'ccourse':
			return cls.__get_ccourse_parser()	
		elif command == 'postasgmnt':
			return cls.__get_postasgmnt_parser()
		elif command == 'rcstudents':
			return cls.__get_rcstudents_parser()				
		elif command == 'newfbmsg':
			return cls.__get_newfbmsg_parser()					
		elif command == 'mkfb':
			return cls.__get_mkfb_parser()			
		
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
	def __get_rcstudents_parser(cls):		
		rcstudents_parser = argparse.ArgumentParser(
			add_help=False,
			prog='rcstudents'
		)
		rcstudents_parser.add_argument(
			'email_domain',
			help="The domain name to which the student's email address resides.\n" \
				"Example: if 'cc.umanitoba.ca' is inserted, the user's email will be " \
				"'dirname@cc.umanitoba.ca', where dirname is the name of the subdirectory."
		)		

		return rcstudents_parser				

	@classmethod
	def __get_newfbmsg_parser(cls):		
		newfbmsg_parser = argparse.ArgumentParser(
			add_help=False,
			prog='newfbmsg'
		)
		newfbmsg_parser.add_argument(
			'alias',
			help="The command that represents the feedback sentence"
		)
		newfbmsg_parser.add_argument(
			'message', 
			help="The feedback sentence to be saved"
		)
		newfbmsg_parser.add_argument(
			'mark_value', 
			type=is_integer_or_float, 
			help="The amount of marks that should be removed when " \
				"using this sentence"
		)

		return newfbmsg_parser

	@classmethod
	def __get_mkfb_parser(cls):		
		mkfb_parser = argparse.ArgumentParser(
			add_help=False,
			prog='mkfb'
		)
		mkfb_parser.add_argument(
			'alias', 
			help="Feedback message alias"
		)
		mkfb_parser.add_argument(
			'student_id',
			help="Student's school unique identifier"
		)
		
		return mkfb_parser		

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