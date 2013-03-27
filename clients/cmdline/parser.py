import argparse

class Parser():

	@classmethod
	def get_parser(cls, command):
		parser = None

		if command == 'newfbmsg':
			return cls.__get_newfbmsg_parser()
		elif command == 'mkfb':
			return cls.__get_mkfb_parser()			
		
		return parser

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
			'school_id',
			help="Student's school unique identifier"
		)
		mkfb_parser.add_argument(
			'alias', 
			help="Feedback message alias"
		)

		return mkfb_parser		

def is_integer_or_float(string):
	try:
		float(string)
	except ValueError:
		raise

	try:
		int(string)
	except ValueError:
		raise

	return string	