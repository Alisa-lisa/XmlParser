from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
import os


app = Flask(__name__)
app.debug = True


import parse

@app.route('/', methods=['POST', 'GET'])
def main():
	if request.method == "POST":
		file = request.files['upload_xml']
		if file:
			path_name = os.path.join('tmp', file.filename)
			file.save(path_name)
			print(parse.analyze_feed(path_name))



	return render_template('main.html')


if __name__ == '__main__':
	app.run(debug=True)