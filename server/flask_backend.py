from flask import render_template
from flask import Flask
from flask import make_response
import topics_extraction_with_nmf_modified
import hashlib
import psycopg2
import os

app = Flask(__name__)

current_topics = extract_topics()

@app.route('/')
def index():
	return render_template('index.html')

# Login page
# Currently assuming users database will contain: email, password (hashed & salted), salt as the first 3 columns
@app.route('/login')
def login():
	# Pull the user's login credentials from the URL and sanitize just in case
	email = check_for_bad_chars(request.args.get('email'))
	password = check_for_bad_chars(request.args.get('password'))
	if email == "BAD STRING" || password == "BAD STRING":
		return render_template('failedlogin.html')

	# Connect to the database and return the user's credentials, if they exist
	conn = psycopg2.connect("dbname=users user=postgres")
	cur = conn.cursor()
	cur.execute("SELECT * FROM users WHERE email=" + email + ";")
	user = cur.fetchone()
	cur.close()
	conn.close()

	# If there is no user, return error
	if user == None:
		return render_template('failedlogin.html')

	# Get that users salt and generate their hashed password
	salt = user[2]
	password = hashlib.sha224(salt + password).hexdigest()

	# If correct password, set a cookie called "email" and redirect to the account page
	# Otherwise send user to failure page
	if password == user[1]:
		resp = make_response(render_template('accountpage.html'))
		resp.set_cookie('email', email)
		return resp
	else
		return render_template('failedlogin.html')

# New user registration page
@app.route('/register', methods=['POST'])
def register():
	# Get the user input data and sanitize inputs
	email = check_for_bad_chars(request.form.get('email'))
	password = check_for_bad_chars(request.form.get('password'))
	if email == "BAD STRING" || password == "BAD STRING":
		return render_template('registerfailure.html')

	# Connect to users database to check if this email already in use
	conn = psycopg2.connect("dbname=users user=postgres")
	cur = conn.cursor()
	cur.execute("SELECT * FROM users WHERE email=" + email + ";")
	user = cur.fetchone()
	cur.close()
	conn.close()

	# Check to make sure the user is not already i nthe database
	if user != None:
		return render_template('registerfailure.html')

	# If not, hash the password with a random salt, and store both the salt and password
	salt = os.urandom
	cur.execute("INSERT INTO users (email, password, salt) VALUES (%s, %s, %s)", (email, hashlib.sha224(salt + password).hexdigest(), salt))
	return render_template('registersuccess.html')


# SQL injections are not fun
# Sanitize your database inputs!
# May not cover all characters; may cover unnecessary characters
def check_for_bad_chars(string):
	bad_chars = ["[", "]", "{", "}", ";", "<", ">", "(", ")"]
	for c in bad_chars:
		if c in string:
			return "BAD STRING"
	return string


