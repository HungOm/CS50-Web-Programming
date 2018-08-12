from flask import Flask , render_template,request, session
from flask_session import Session


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session (app)

# notes = []


@app.route('/', methods=["GET","POST"])
def index():
	# return "Hello, World!

	# headline = "My page!"

	# return render_template('index.html', headline=headline)
	# names = ['Alice','Bob', 'Chalie', 'David', 'Hung Om']

	# return render_template('index.html')
	# session["notes"] = []

	if session.get("notes") is None:
		session["notes"] = []

	if request.method == "POST":
		note = request.form.get("note")
		session["notes"].append(note)

	return render_template("index.html", notes=session["notes"])

@app.route('/more')
def more():
	return render_template('more.html')



# @app.route('/hello', methods=["GET","POST"])
# def hello():
# 	if request.method=="GET":
# 		return "Please submit the form intead."
# 	else:
# 		name = request.form.get("name")
# 		return render_template("hello.html", name=name)




# @app.route('/david')

# def david():
# 	return "Hello , David!"

# @app.route('/maria')
# def maria():
# # 	return "Hello Maria!"

# @app.route('/<string:name>')
# def hello(name):
# 	return "hello , {}!".format(name)