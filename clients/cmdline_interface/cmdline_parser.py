import argparse

class Parser():

	@classmethod
	def get_parser(cls, command):
		parser = None

		if command == 'newfbmsg':
			return cls.__get_newfbmsg_parser()
		
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

def is_integer_or_float(string):
	is_integer = False
	is_float = False

	try:
		float(string)
		is_float = True
	except ValueError:
		is_float = False

	try:
		int(string)
		is_integer = True
	except ValueError:
		is_integer = False

	return is_integer or is_float	