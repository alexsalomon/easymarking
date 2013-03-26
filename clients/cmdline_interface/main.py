#!/usr/bin/python

import cmd
from cmdline_parser import Parser
from engine.feedback_message import save_message

class CmdlineInterface(cmd.Cmd):

	intro = 'EasyMarking v1.0 - Type "help" for help.\n' \
		'Good marking! :)\n'
	prompt = "easyMarker=# "

	def help_newfbmsg(self): Parser.get_parser('newfbmsg').print_help()
	def do_newfbmsg(self, line):
		try:
			parser = Parser.get_parser('newfbmsg')
			args = parser.parse_args(line.split())
			save_message(args.alias, args.message, args.mark_value)
		except SystemExit:
			print ""
			return None	

	def default(self, line):
		print "*** Unknown command: " + line
		print ""

	def do_exit(self, line):
		return True;		

	def do_quit(self, line):
		return True;

	def do_EOF(self, line):
		print "\n"
		return True	
