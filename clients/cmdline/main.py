#!/usr/bin/python

import cmd, shlex, os, subprocess
from parser import Parser
from engine.reports import reports_api
from engine.feedback_message import save_message, append_feedback
from engine.marking_setup import create_course, post_assignment, initiate_marking
from engine.dir_navigation import navigate_to_next_directory, navigate_to_prev_directory, change_directory

class CmdlineInterface(cmd.Cmd):

	intro = 'EasyMarking v1.0 - Type "help" for help.\n' \
		'Good marking! :)\n'
	base_prompt = "easyMarker=# "
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

	def help_init(self): Parser.get_parser('init').print_help()
	def do_init(self, line):
		try:
			parser = Parser.get_parser('init')
			args = parser.parse_args(shlex.split(line))
			print create_course(args.course_id)			
			print post_assignment(
				args.course_id, 
				args.assignment_number,
				args.maximum_marks
			)
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

	# def help_gensrep(self): Parser.get_parser('gensrep').print_help()
	# def do_gensrep(self, line):
	# 	try:
	# 		parser = Parser.get_parser('gensrep')
	# 		args = parser.parse_args(shlex.split(line))
	# 		reports_api.generate_all_individual_student_fd_reports_for_assignment(
	# 			args.course_id, 
	# 			args.assignment_number
	# 		)
	# 	except SystemExit:
	# 		pass

	def help_genfrep(self): Parser.get_parser('genfrep').print_help()
	def do_genfrep(self, line):
		try:
			parser = Parser.get_parser('genfrep')
			args = parser.parse_args(shlex.split(line))
			reports_api.generate_overall_feedback_report_for_assignment(
				args.course_id, 
				args.assignment_number
			)
		except SystemExit:
			pass			

	def help_genagrep(self): Parser.get_parser('genagrep').print_help()
	def do_genagrep(self, line):
		try:
			parser = Parser.get_parser('genagrep')
			args = parser.parse_args(shlex.split(line))
			reports_api.generate_grades_report_for_assignment(
				args.course_id, 
				args.assignment_number
			)
		except SystemExit:
			pass

	def help_gencgrep(self): Parser.get_parser('gencgrep').print_help()
	def do_gencgrep(self, line):
		try:
			parser = Parser.get_parser('gencgrep')
			args = parser.parse_args(shlex.split(line))
			reports_api.generate_xls_grades_report_for_course(
				args.course_id, 
				args.assignment_number
			)
		except SystemExit:
			pass			

	def help_genallreps(self): Parser.get_parser('genallreps').print_help()
	def do_genallreps(self, line):
		try:
			parser = Parser.get_parser('genallreps')
			args = parser.parse_args(shlex.split(line))
			reports_api.generate_all_reports(args.course_id, args.assignment_number)
		except SystemExit:
			pass

	def help_sendallemails(self): Parser.get_parser('sendallemails').print_help()
	def do_sendallemails(self, line):
		try:
			parser = Parser.get_parser('sendallemails')
			args = parser.parse_args(shlex.split(line))
			reports_api.generate_all_reports(args.course_id, args.assignment_number)
			# email.send_email_feedback_email_to_all_students_who_handed_assignments(
			# 	args.course_id, 
			# 	args.assignment_number
			# )
			email.send_email_to_professor_with_overall_feedback_and_grades(
				args.course_id, 
				args.assignment_number
			)
		except SystemExit:
			pass				

	def do_cd(self, line):
		try:
			line = os.path.expanduser(line)
			change_directory(line)
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
