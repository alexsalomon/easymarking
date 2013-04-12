#!/usr/bin/python

import cmd, shlex, os, subprocess
from parser import Parser
from engine.reports import generate_individual_student_feedback_report
from engine.feedback_message import save_message, append_feedback
from engine.marking_setup import create_course, post_assignment

class CmdlineInterface(cmd.Cmd):

	intro = 'EasyMarking v1.0 - Type "help" for help.\n' \
		'Good marking! :)\n'
	prompt = "easyMarker=# "

	def help_ccourse(self): Parser.get_parser('ccourse').print_help()
	def do_ccourse(self, line):
		try:
			parser = Parser.get_parser('ccourse')
			args = parser.parse_args(shlex.split(line))
			print create_course(
				args.course_id, 
				args.course_name,
				args.prof_name, 
				args.prof_email
			)
		except SystemExit:
			pass

	def help_ccourse(self): Parser.get_parser('postasgmnt').print_help()
	def do_postasgmnt(self, line):
		try:
			parser = Parser.get_parser('postasgmnt')
			args = parser.parse_args(shlex.split(line))
			print post_assignment(
				args.course_id, 
				args.assignment_number,
				args.maximum_marks
			)
		except SystemExit:
			pass			

	def help_newfbmsg(self): Parser.get_parser('newfbmsg').print_help()
	def do_newfbmsg(self, line):
		try:
			parser = Parser.get_parser('newfbmsg')
			args = parser.parse_args(shlex.split(line))
			print save_message(args.alias, args.message, args.mark_value)
		except SystemExit:
			pass

	def help_mkfb(self): Parser.get_parser('mkfb').print_help()
	def do_mkfb(self, line):
		try:
			parser = Parser.get_parser('mkfb')
			args = parser.parse_args(shlex.split(line))
			print append_feedback(
				args.alias, 
				args.student_id, 
				"COMP 4350", 
				1, 
				100
			)
		except SystemExit:
			pass

	#def help_sturep(self): Parser.get_parser('mkfb').print_help()
	def do_sturep(self, line):
		generate_individual_student_feedback_report('umkonkin', "COMP 4350", 1)

	def do_cd(self, line):
		try:
			# if line.startswith("~"): 
			# 	line = line.replace("~", os.path.expanduser('~'), 1)
			line = os.path.expanduser(line)

			os.chdir(line)
		except OSError as e:
			print "cd: " + e.filename + ": " + e.strerror

	def default(self, line):
		subprocess.call(line, shell=True)

	def do_exit(self, line):
		return True;		

	def do_quit(self, line):
		return True;

	def do_EOF(self, line):
		print "\n"
		return True	
