import os
from flask import Flask, render_template, request, redirect
from flask import url_for
from werkzeug import secure_filename
import upload

app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def index(name=None):
	return render_template('index.html', name=name)
	

@app.route('/upload', methods=['GET', 'POST'])
@app.route('/<user_name>/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and upload.allowed_file(file.name):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file', filename=filename))

	return render_template('upload.html')


if __name__ == '__main__':
	app.run()
