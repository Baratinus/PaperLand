from flask import Flask,render_template,request,redirect,url_for,flash,session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

from . import db
from . import models
from . import mail
from . import passwordcheck

app = Flask(__name__)
app.secret_key = b'\xd7\xbd\xa4\xdf\xbd\x0e\xdds\xdd\xdd\x03\x1f\xc9\xe1\xa4U'

app.config.from_object('config')

@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")


@app.route('/404/')
def err404():
    return render_template("404.html")


@app.route('/panier/')
def panier():
    return render_template("panier.html")


@app.route('/register/', methods=['POST', 'GET']) # Ancien register-succes
def register():
    if request.method == 'GET' :
        return render_template("register.html")

    else :
        user = models.User()

        if (user.check_value("pseudo", request.form["pseudo"]) or user.check_value("email", request.form["email"])):
            flash("Pseudo ou email déjà existant", "error")
            return redirect(url_for('login'))

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
            if len(request.form["firstname"]) == 0 :
                user.firstname = 'Unknown'
            if len(request.form["lastname"]) == 0 :
                user.lastname = 'Unknown' 
            if len(request.form["adresse"]) == 0 :
                user.adress = 'Unknown'
            if len(request.form["ville"]) == 0 :
                user.city = 'Unknown'
            if len(request.form["cp"]) == 0 :
                user.postalcode = 'Unknown'
            if len(request.form["telephone"]) == 0 :
                user.phone = 'Unknown'

            if passwordcheck.checkPassword((request.form["password"])) == True :
                user.password = generate_password_hash(request.form["password"], method='sha256', salt_length=8)
                user.add_user_in_database()
            else : 
                flash("Mot de passe Invalide", "error")
                return redirect(url_for('register'))
           
            
            # Connexion lors de l'enregistrement
            session["user"] = user.pseudo

            return render_template("register-successfully.html")


@app.route('/login/', methods=['POST','GET'])
def login():

    if request.method == 'GET' :
        return render_template("login.html")
    
    else :
        user = db.get_user("email", request.form["email"])

        if user == None:
            flash("Identifiants incorrects, veuillez vérifier votre email et mot de passe.", "error") #Cas adresse email inexistante.
            return redirect(url_for('login'))
        
        elif check_password_hash(user.password, request.form["password"]) == True:
            session["user"] = user.pseudo
            print(session["user"])
            return render_template("login-successfully.html")

        else:
            flash("Identifiants incorrects, veuillez vérifier votre email et mot de passe.", "error") #Cas mot de passe incorrect.
            return redirect(url_for('login'))


@app.route('/logout/', methods=['GET'])
def logout():

    try:
        session["user"]
        session.clear()
    except KeyError :
        return render_template("pleaseconnect.html")
    else:
        return render_template("logout-succesfully.html")


@app.route('/lostpassword/', methods=['POST', 'GET'])
def lost_password():

    if request.method == 'GET' :
        return render_template("lostpassword.html")

    else :

        user = db.get_user("email", request.form['email'])
        if user != None and user.check_value("email", request.form['email'] ) == True and user.check_value("datebirthday", request.form['birthday']) == True :
            new_password = str(uuid4())
            user = db.get_user('email', request.form['email'])
            user.password = generate_password_hash(new_password, method='sha256', salt_length=8)
            user.modify_password_in_database()
            mail.sendmail(request.form['email'],new_password)
            
        else :
            pass

        return render_template("lostpasswordresults.html", email = request.form['email'], birthday = request.form['birthday'])
        


@app.route('/modifypassword/', methods=['POST'])
def modifypassword():

    user = models.User()
    user.pseudo = session["user"]
    if passwordcheck.checkPassword((request.form["password"])) == True :
            user.password = generate_password_hash(request.form["password"], method='sha256', salt_length=8)
            user.modify_password_in_database()
            return render_template("profil.html")
    else :
        flash("Le mot de passe n'est pas valide", "error")
        return redirect(url_for('profil'))
    

@app.route('/profil/', methods=['GET'])
def profil():
    try:
        session["user"]
    except KeyError:
        return redirect(url_for('login'))
    else:
        user_ = db.get_user('pseudo', session['user'])
        return render_template("profil.html", user=user_)


app.run(debug=True, port=app.config["PORT"], host=app.config["IP"])