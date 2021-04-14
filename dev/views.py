from flask import Flask,render_template,request,redirect,url_for,flash

from . import db
from . import models
from . import mail

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

@app.route('/forgotpassword/', methods=['POST', 'GET'])
def forgotpasswordresult():
    # user = models.User() TODO FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME
    if request.method == 'GET' :
        return render_template("forgotpassword.html")
    else :
        result = request.form
        email = result['email']
        birthday = result['birthday']
        # if user.check_email(email) == True and user.check_birthday(birthday) == True : 
        #     mail.sendmail(email,(user.get_password(email, birthday)))
        # else :
        #     pass TODO FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME
        mail.sendmail(email, 'testpassword_to_implement')
        return render_template("forgotpasswordresults.html", email = email, birthday = birthday)

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
    # pas très propre (tkt on corrigera ça au fur et à mesure (j'en ai rajouté un L23) 'Max')
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

@app.route('/panier/')
def panier():
    return render_template("panier.html")

@app.route('/profil/')
def profil():
    return render_template("profil.html")

app.run(debug=True, port=app.config["PORT"], host=app.config["IP"])