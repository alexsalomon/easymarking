import os, os.path

def navigate_to_next_directory():
	curr_dir = os.getcwd()
	curr_dir_basename = os.path.basename(curr_dir)
	parent_dir = os.path.dirname(curr_dir)
	parent_subdirectory_names = get_immediate_subdirectories(parent_dir)	
	curr_dir_index = parent_subdirectory_names.index(curr_dir_basename)
	next_dir_basename = parent_subdirectory_names[curr_dir_index+1]
	os.chdir(parent_dir+"/"+next_dir_basename)
	return "Switched to '" + os.getcwd() + "'"

def navigate_to_prev_directory():
	curr_dir = os.getcwd()
	curr_dir_basename = os.path.basename(curr_dir)
	parent_dir = os.path.dirname(curr_dir)
	parent_subdirectory_names = get_immediate_subdirectories(parent_dir)	
	curr_dir_index = parent_subdirectory_names.index(curr_dir_basename)
	next_dir_basename = parent_subdirectory_names[curr_dir_index-1]
	os.chdir(parent_dir+"/"+next_dir_basename)
	return "Switched to '" + os.getcwd() + "'"

def get_immediate_subdirectories(dir):
    return [filename for filename in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, filename))]