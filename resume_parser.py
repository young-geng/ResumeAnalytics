""" Python program to read .txt resume files and puts them into sqlite database table of 2 columns.
	ID(integer) and Resume(txt)."""

import inspect
import sys
import sqlite3
import re


def main(fn):
    """Call fn with command line arguments.  Used as a decorator.

    The main decorator marks the function that starts a program. For example,

    @main
    def my_run_function():
        # function body

    Use this instead of the typical __name__ == "__main__" predicate.
    """
    if inspect.stack()[1][0].f_locals['__name__'] == '__main__':
        args = sys.argv[1:] # Discard the script name from command line
        fn(*args) # Call the main function
    return fn


def get_resume_dict(input_args):
	print("Fetching resumes.")
	resume_id = 0
	return_dict = {}
	while input_args:
		open_file = open(input_args[0], 'r')
		return_dict[resume_id] = re.sub(r'[^ -~]+', ' ', open_file.read()).encode('ascii', 'ignore')
		input_args.pop(0)
		resume_id += 1
		open_file.close()

	return return_dict


def put_in_db(inputs_list):
	print("Creating a database")
	if not len(inputs_list):
		print ("No input is given")
		raise EOFError

	inputs_list = list(inputs_list)
	connection = sqlite3.connect('resumes.db')
	cursor = connection.cursor()
	
	resume_dict = get_resume_dict(inputs_list)
	# convert into list of 2 pair tuples
	resume_file_list = [(key, resume_dict[key]) for key in resume_dict.keys()]

	# drop if it exists and create table in db
	cursor.execute("DROP TABLE IF EXISTS resumes")
	cursor.execute(''' CREATE TABLE resumes
						(id real, resume text)''')

	# Insert rows of data to our table in single time from list of data
	cursor.executemany('INSERT INTO resumes VALUES (?,?)', resume_file_list)
	connection.commit()

	connection.close()

@main
def run(*args):
	print ("The program has started.")
	put_in_db(args)
