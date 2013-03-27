#!/usr/bin/python

import cmd, shlex
from parser import Parser
from engine.feedback_message import save_message, append_feedback

class CmdlineInterface(cmd.Cmd):

	intro = 'EasyMarking v1.0 - Type "help" for help.\n' \
		'Good marking! :)\n'
	prompt = "easyMarker=# "

	def help_newfbmsg(self): Parser.get_parser('newfbmsg').print_help()
	def do_newfbmsg(self, line):
		try:
			parser = Parser.get_parser('newfbmsg')
			args = parser.parse_args(shlex.split(line))
			print save_message(args.alias, args.message, args.mark_value)
		except SystemExit:
			print ""

	def help_mkfb(self): Parser.get_parser('mkfb').print_help()
	def do_mkfb(self, line):
		try:
			parser = Parser.get_parser('mkfb')
			args = parser.parse_args(shlex.split(line))
			print append_feedback(args.school_id, args.alias)
		except SystemExit:
			print ""			

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
