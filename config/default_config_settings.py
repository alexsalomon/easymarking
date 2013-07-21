from database_models.system_configuration import SystemConfiguration

def fill_database_with_default_config_settings():

	#Template Path Defaults:
	SystemConfiguration.set_setting('templates_directory_path', ??)

	#Email Defaults:
	SystemConfiguration.set_setting('marker_email', None)
	SystemConfiguration.set_setting('email_host', 'localhost')
	SystemConfiguration.set_setting('email_host_username', None)
	SystemConfiguration.set_setting('email_host_password', None)

	student_email_template_file_path