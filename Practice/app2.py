from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return render_template('login.html',  title="Form sample",  message="お名前は？")

@app.route('/', methods=['POST'])
def form():
	field = request.form['field']
	return render_template('login.html', title="Form sample",  message="こんにちは、%s さん！" % field)

if __name__ == '__main__':
	app.debug = True
	app.run(host='localhost') 