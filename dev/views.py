from flask import Flask,render_template,request

app = Flask(__name__)

app.config.from_object('config')

@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")

@app.route('/register/')
def register():
    return render_template("register.html")

@app.route('/login/')
def login():
    return render_template("login.html")

app.run(debug=True, port=app.config["PORT"], host=app.config["IP"])