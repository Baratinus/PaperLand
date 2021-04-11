from flask import Flask,render_template,request,redirect,url_for,flash

<<<<<<< Updated upstream
=======
from . import db
from . import models

>>>>>>> Stashed changes
app = Flask(__name__)
app.secret_key = b'\xd7\xbd\xa4\xdf\xbd\x0e\xdds\xdd\xdd\x03\x1f\xc9\xe1\xa4U'

app.config.from_object('config')

@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")

@app.route('/register/', methods=['POST', 'GET'])
def register():
    return render_template("register.html")

@app.route('/login/', methods=['POST', 'GET'])
def login():
    return render_template("login.html")

@app.route('/connection-successfully/', methods=['POST', 'GET'])
def connection_successfully():
    print(request.form)
    for k in request.form:
        print(k)
    return render_template("connection-successfully.html")

@app.route('/register-successfully/', methods=['POST', 'GET'])
def register_successfully():
    user = models.User()
    # pas très propre
    try:
        user.pseudo = request.form["pseudo"]
        user.firstname = request.form["firstname"]
        user.lastname = request.form["lastname"]
        user.sexe = request.form["sexe"]
        user.email = request.form["email"]
        user.adress = request.form["adresse"]
        user.city = request.form["ville"]
        user.postalcode = request.form["cp"]
        user.phone = request.form["telephone"]
        user.datebirthday = request.form["birthday"]
        user.password = request.form["password"]
    except ValueError:
        flash("Pseudo ou email déjà existant", "error")
        return redirect(url_for('register'))
    else:
        user.add_user_in_database()
        return render_template("register-successfully.html")

@app.route('/404/')
def err404():
    return render_template("404.html")

app.run(debug=True, port=app.config["PORT"], host=app.config["IP"])