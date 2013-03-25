#!/usr/bin/python

import cmd
from engine.feedback_message import save_message

class CmdlineInterface(cmd.Cmd):

	intro = 'EasyMarking v1.0 - Type "help" for help.\n' \
		'Good marking! :)\n'
	prompt = "easyMarker=# "

	def do_newfbmsg(self, line):
		"Saves a new custom feedback message"
		save_message(line)

	def default(self, line):
		print "*** Unknown command: " + line

	def do_exit(self, line):
		return True;		

	def do_quit(self, line):
		return True;

	def do_EOF(self, line):
		print "\n"
		return True

if __name__ == '__main__':
    CmdlineInterface().cmdloop()
