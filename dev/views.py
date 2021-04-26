from flask import Flask,render_template,request,redirect,url_for,flash,session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

from . import db
from . import models
from . import mail
from . import passwordcheck
from . import pseudocheck

app = Flask(__name__)
app.secret_key = b'\xd7\xbd\xa4\xdf\xbd\x0e\xdds\xdd\xdd\x03\x1f\xc9\xe1\xa4U'

app.config.from_object('config')


@app.route('/')    
@app.route('/index/')
def index():
    return render_template("index.html", user_pseudo = getpseudo())


@app.errorhandler(404)
def err404(error):
    return render_template('404.html', user_pseudo = getpseudo())


@app.route('/panier/')
def panier():
    return render_template("panier.html", user_pseudo = getpseudo())


@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'GET' :
        return render_template("register.html")

    else :
        user = models.User()
        if pseudocheck.checkPseudo((request.form['pseudo'])) == True :
            user.pseudo = request.form["pseudo"]
        else :
            flash("Pseudo Invalide, Recommencez", "error")
            return redirect(url_for('register'))   

        if (user.check_value("pseudo", request.form["pseudo"]) or user.check_value("email", request.form["email"])):
            flash("Pseudo ou email déjà existant", "error")
            return redirect(url_for('login'))

        else:
            user.firstname = request.form["firstname"].capitalize()
            user.lastname = request.form["lastname"].upper()
            user.sexe = request.form["sexe"]
            user.email = request.form["email"]
            user.adress = str(request.form["adresse"])
            user.city = request.form["ville"]
            user.postalcode = request.form["cp"]
            user.phone = request.form["telephone"]
            user.datebirthday = request.form["birthday"]
            user.temporarypassword = "NO"


            if passwordcheck.checkPassword((request.form["password"])) == True :
                user.password = generate_password_hash(request.form["password"], method='sha256', salt_length=8)
                user.add_user_in_database()
                mail.sendmail(user.email,"NONE",'notify_account_created')
            else : 
                flash("Mot de passe invalide", "error")
                return redirect(url_for('register'))
           
            # Connexion lors de l'enregistrement
            session["user"] = user.pseudo

            return render_template("register-successfully.html", user_pseudo = getpseudo())


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
            if user.temporarypassword == "YES" :
                return render_template("pleasechangepassword.html", user_pseudo = getpseudo())
            else :
                return render_template("login-successfully.html", user_pseudo = getpseudo())

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
        return render_template("logout-succesfully.html", user_pseudo = '')


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
            user.set_temporary_password_state_yes_in_database()
            mail.sendmail(request.form['email'],new_password)
            
        else :
            pass

        return render_template("lostpasswordresults.html", email = request.form['email'], birthday = request.form['birthday'])
        

@app.route('/modifypassword/', methods=['POST'])
def modifypassword():
    user_ = db.get_user('pseudo', getpseudo())
    if passwordcheck.checkPassword((request.form["password"])) == True :
            user_.password = generate_password_hash(request.form["password"], method='sha256', salt_length=8)
            user_.modify_password_in_database()
            user_.set_temporary_password_state_no_in_database()
            mail.sendmail(user_.email,"NONE",'notify_update_password')
            return redirect(url_for('profil', user=user_, user_pseudo = getpseudo()))
    else :
        flash("Le mot de passe n'est pas valide !", "error")
        return redirect(url_for('profil', user=user_, user_pseudo = getpseudo() ))


@app.route('/modify-personal-informations/', methods=['GET', 'POST'])
def modify_personal_informations():
    if request.method == 'GET' :
        return render_template("modify-personal-informations.html")
    
    else :
        try :
            session["user"]
        except KeyError:
            return redirect(url_for('login'))
        else :            
            user_ = db.get_user('pseudo', getpseudo())

            if (user_.check_value("email", request.form["email"])):
                flash("Email déjà existant, réessayez", "error")
                return redirect(url_for('modify_personal_informations'))

            if len(request.form["firstname"]) == 0 :
                user_.firstname = user_.firstname
            else :
                user_.firstname = request.form["firstname"].capitalize()

            if len(request.form["lastname"]) == 0 :
                user_.lastname = user_.lastname
            else :
                user_.lastname = request.form["lastname"].upper()

            if len(request.form["sexe"]) == 0 :
                user_.sexe = user_.sexe
            else :
                user_.sexe = request.form["sexe"]
            
            if len(request.form["email"]) == 0 :
                user_.email = user_.email
            else :
                user_.email = request.form["email"]
            
            if len(request.form["adresse"]) == 0 :
                user_.adress = user_.adress
            else :
                user_.adress = str(request.form["adresse"])
            
            if len(request.form["ville"]) == 0 :
                user_.city = user_.city
            else :
                user_.city = request.form["ville"]
            
            if len(request.form["cp"]) == 0 :
                user_.postalcode = user_.postalcode
            else :
                user_.postalcode = request.form["cp"]
            
            if len(request.form["telephone"]) == 0 :
                user_.phone = user_.phone
            else :
                user_.phone = request.form["telephone"]
            
            if len(request.form["birthday"]) == 0 :
                user_.datebirthday = user_.datebirthday
            else :
                user_.datebirthday = request.form["birthday"]

            user_.modify_personal_informations_in_database()
            return render_template("account-succesfully-modified.html", user_pseudo = getpseudo())


@app.route('/deleteaccount/', methods=['GET','POST'])
def deleteaccount():

    if request.method == 'GET' :
        return render_template('deleteaccount.html')
    else :
        user_ = db.get_user('pseudo', getpseudo())
        if request.form['delete-account'] == "Oui" :
            user_.delete_account_in_database()
            mail.sendmail(user_.email,"NONE",'notify_account_deleted')
            session.clear()
            return render_template("account-succesfully-deleted.html", user_pseudo = getpseudo())
        else :
            return redirect(url_for('profil', user=user_, user_pseudo = getpseudo()))


@app.route('/profil/', methods=['GET'])
def profil():
    try:
        session["user"]
    except KeyError:
        return redirect(url_for('login'))
    else:
        user_ = db.get_user('pseudo', session['user'])
        if len(user_.firstname) == 0 :
            user_.firstname = 'Unknown'
        if len(user_.lastname) == 0 :
            user_.lastname = 'Unknown' 
        if len(user_.adress) == 0 :
            user_.adress = 'Unknown'
        if len(user_.city) == 0 :
            user_.city = 'Unknown'
        if len(user_.postalcode) == 0 :
            user_.postalcode = 'Unknown'
        if len(user_.phone) == 0 :
            user_.phone = 'Unknown'
        user_.datebirthday = formatdateprofil()
        user_.phone = formatphoneprofil()

        return render_template("profil.html", user=user_ , user_pseudo = getpseudo())


@app.route('/<category>')
def category(category:str):
    return render_template("category.html", category=category, products=db.get_products_in_category(category))


@app.route('/<category>/<id_product>')
def product(category:str, id_product:int):
    return render_template("product.html", product=db.get_product_by_id(id_product))

### PARTIE UTILITAIRES ###
def getpseudo():
    try :
        session["user"]
    except KeyError :
        user_session = ''
    else :
        user_ = db.get_user('pseudo', session['user'])
        user_session = user_.pseudo        
    return user_session


def formatdateprofil():
    user_ = db.get_user('pseudo', session['user'])
    birthdate = user_.datebirthday.split("-")
    new_birthday = birthdate[2] + '-' + birthdate[1] + '-' + birthdate[0]
    return new_birthday


def formatphoneprofil():
    user_ = db.get_user('pseudo', session['user'])
    phonenumber = user_.phone
    if len(phonenumber) == 12 :
        new_phonenumber = phonenumber[:3] + ' ' + phonenumber[-9:-8] + ' ' + phonenumber[-8:-6] + ' ' + phonenumber[-6:-4] + ' ' + phonenumber[-4:-2] + ' ' + phonenumber[-2:]
        return new_phonenumber
    elif len(phonenumber) == 10 :
        return phonenumber[:2] + ' ' + phonenumber[-8:-6] + ' ' + phonenumber[-6:-4] + ' ' + phonenumber[-4:-2] + ' ' + phonenumber[-2:]
    else :
        return user_.phone


### PARTIE ADMIN ###
@app.route('/admin/', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        if request.form['password'] == 'admin':
            session['admin'] = True
        
    try:
        if session["admin"] == True:
            return render_template('admin/general.html')
        else:
            return render_template('admin/login.html')
    except KeyError:
        return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    session['admin'] = False
    return redirect(url_for('index'))


@app.route('/admin/produit', methods=['POST', 'GET'])
def admin_view_product():
    try:
        if session['admin'] == True:
            return render_template('admin/product-view.html', products=db.get_table("Product"))
    except KeyError:
        return redirect(url_for('index'))


@app.route('/admin/produit/<product_id>')
def admin_modify_product(product_id:int): 
    try:
        if session['admin'] == True:
            return render_template('admin/product-modify.html', product=db.get_product_by_id(product_id))
    except KeyError:
        return redirect(url_for('index'))


@app.route('/admin/produit/nouveau-produit', methods=['POST', 'GET'])
def admin_new_product():
    try:
        if session['admin'] == True:
            return render_template('admin/product-append.html')
    except KeyError:
        return redirect(url_for('index'))


@app.route('/admin/produit/nouveau-produit-request', methods=['POST', 'GET'])
def admin_new_product_request():
    if request.method == "POST":
        product = models.Product()
        product.name = request.form["name"]
        product.category = request.form["category"]
        product.price = float(request.form["price"])
        product.image = request.form["image"]
        product.description = request.form["description"]
        product.add_product_in_database()
        return redirect(url_for('admin_view_product'))
    else:
        pass


app.run(debug=True, port=app.config["PORT"], host=app.config["IP"])