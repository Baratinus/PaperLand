from . import mail
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
# ----------------------------------------------- TODO RASSEMBLER ----------------------------------------------
@app.route('/forgotpassword/', methods=['GET'])
def forgotpassword():
    return render_template("forgotpassword.html")

@app.route('/forgotpassword/', methods=['POST'])
def forgotpasswordresult():
    result = request.form
    email = result['email']
    birthday = result['birthday']
    mail.sendmail(email,"password_test") # TODO A IMPLEMENTER TEST BD AVEC DATE DE NAISSANCE + MDP DEPUIS LA BD 
    return render_template("forgotpasswordresults.html", email = email, birthday = birthday)
# -------------------------------------------------------------------------------------------------------------------------
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