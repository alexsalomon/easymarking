#!/usr/bin/python

import cmd

class Interface(cmd.Cmd):

	intro = 'EasyMarking v1.0 - Type "help" for help.\n' \
		'Good marking! :)\n'
	prompt = "easyMarker=# "

	def do_say(self, line):
		"Repeats whatever the user types"
		print line 

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
    Interface().cmdloop()
