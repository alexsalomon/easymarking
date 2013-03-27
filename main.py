#!/usr/bin/python

from clients.cmdline_interface import main 
from database_models import database

database.init()

if __name__ == '__main__':
	main.CmdlineInterface().cmdloop()
