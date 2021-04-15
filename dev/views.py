from flask import Flask,render_template,request,redirect,url_for,flash,session

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
    if request.method == 'GET' :
        return render_template("forgotpassword.html")
    else :
        user = db.get_user("email", request.form['email'])
        if user.check_value("email", request.form['email'] ) == True and user.check_value("datebirthday", request.form['birthday']) == True :
            mail.sendmail(request.form['email'],str(user.password))
        else :
            pass

        return render_template("forgotpasswordresults.html", email = request.form['email'], birthday = request.form['birthday'])

@app.route('/login/', methods=['POST', 'GET'])
def login():
    return render_template("login.html")

@app.route('/connection-successfully/', methods=['POST', 'GET'])
def connection_successfully():
    user = db.get_user("email", request.form["email"])
    print(user)

    if user == None:
        flash("Adresse mail inexistante", "error")
        return redirect(url_for('login'))
    
    elif user.password == request.form["password"]:
        session["user"] = user.pseudo
        print(session["user"])
        return render_template("connection-successfully.html")

    else:
        flash("Mot de passe incorrect", "error")
        return redirect(url_for('login'))


@app.route('/register-successfully/', methods=['POST', 'GET'])
def register_successfully():
    user = models.User()
    # pas très propre (tkt on corrigera ça au fur et à mesure (j'en ai rajouté un L23) 'Max')
    # try:
    #     user.pseudo = request.form["pseudo"]
    #     user.firstname = request.form["firstname"]
    #     user.lastname = request.form["lastname"]
    #     user.sexe = request.form["sexe"]
    #     user.email = request.form["email"]
    #     user.adress = request.form["adresse"]
    #     user.city = request.form["ville"]
    #     user.postalcode = request.form["cp"]
    #     user.phone = request.form["telephone"]
    #     user.datebirthday = request.form["birthday"]
    #     user.password = request.form["password"]
    # except ValueError:
    #     flash("Pseudo ou email déjà existant", "error")
    #     return redirect(url_for('register'))
    # else:
    #     user.add_user_in_database()
    #     return render_template("register-successfully.html")

    # vérification des valeurs uniques
    print(user.check_value("pseudo", request.form["pseudo"]))
    print(user.check_value("email", request.form["email"]))
    if (user.check_value("pseudo", request.form["pseudo"]) or user.check_value("email", request.form["email"])):
        flash("Pseudo ou email déjà existant", "error")
        return redirect(url_for('register'))
    else:
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
    try:
        session["user"]
    except KeyError:
        return redirect(url_for('login'))
    else:
        return render_template("profil.html")

@app.route('/disconnect/')
def disconnect():
    try:
        session.clear()
    except :
        return redirect(url_for('err404'))
    else:
        return render_template("disconnected-succesfully.html")

app.run(debug=True, port=app.config["PORT"], host=app.config["IP"])