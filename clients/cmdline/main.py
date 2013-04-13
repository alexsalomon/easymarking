#!/usr/bin/python

import cmd, shlex, os, subprocess
from parser import Parser
from engine.reports import generate_individual_student_feedback_report
from engine.feedback_message import save_message, append_feedback
from engine.marking_setup import create_course, post_assignment
from engine.marking_setup import initiate_marking
from engine.dir_navigation import navigate_to_next_directory, navigate_to_prev_directory

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

	def help_postasgmnt(self): Parser.get_parser('postasgmnt').print_help()
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

	def help_initmarking(self): Parser.get_parser('initmarking').print_help()
	def do_initmarking(self, line):
		try:
			parser = Parser.get_parser('initmarking')
			args = parser.parse_args(shlex.split(line))
			print initiate_marking(
				args.course_id,
				args.assignment_number,
				args.email_domain
			)
		except SystemExit:
			pass						

	def help_newfd(self): Parser.get_parser('newfd').print_help()
	def do_newfd(self, line):
		try:
			parser = Parser.get_parser('newfd')
			args = parser.parse_args(shlex.split(line))
			print save_message(args.alias, args.message, args.mark_value)
		except SystemExit:
			pass

	def help_fd(self): Parser.get_parser('fd').print_help()
	def do_fd(self, line):
		try:
			parser = Parser.get_parser('fd')
			args = parser.parse_args(shlex.split(line))
			print append_feedback(
				args.alias, 
				args.student_id
			)
		except SystemExit:
			pass

	#def help_sturep(self): Parser.get_parser('fd').print_help()
	def do_sturep(self, line):
		generate_individual_student_feedback_report('umkonkin', "COMP 4350", 1)

	def do_cd(self, line):
		try:
			line = os.path.expanduser(line)
			os.chdir(line)
		except OSError as e:
			print "cd: " + e.filename + ": " + e.strerror

	def help_nextdir(self): Parser.get_parser('nextdir').print_help()
	def do_next(self, line): return self.do_nextdir(line)
	def do_nextdir(self, line):
		try:
			parser = Parser.get_parser('nextdir')
			args = parser.parse_args(shlex.split(line))
			print navigate_to_next_directory()
		except SystemExit:
			pass	

	def help_prevdir(self): Parser.get_parser('prevdir').print_help()
	def do_prev(self, line): return self.do_prevdir(line)
	def do_prevdir(self, line):
		try:
			parser = Parser.get_parser('prevdir')
			args = parser.parse_args(shlex.split(line))
			print navigate_to_prev_directory()
		except SystemExit:
			pass					

	def default(self, line):
		subprocess.call(line, shell=True)

	def do_EOF(self, line): print ""; return self.do_exit(line)
	def do_quit(self, line): return self.do_exit(line)
	def do_exit(self, line): return True
