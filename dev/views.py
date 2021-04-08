from flask import Flask,render_template,request

from . import db

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

@app.route('/404/')
def err404():
    return render_template("404.html")

@app.route('/panier/')
def panier():
    return render_template("panier.html")

app.run(debug=True, port=app.config["PORT"], host=app.config["IP"])