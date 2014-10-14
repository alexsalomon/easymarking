#!/usr/bin/python

from clients.cmdline import main 
from database_models import database
#from config.default_config_settings import fill_database_with_default_config_settings

database.init()

if __name__ == '__main__':
	#fill_database_with_default_config_settings()
	main.CmdlineInterface().cmdloop()
