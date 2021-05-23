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
@app.route('/index/', methods=['GET'])
def index():
    """page accueil
    """
    return render_template("index.html", user_pseudo = getpseudo(), user_admin = getadminstate(), products_cahiers = db.get_products_in_category('cahiers'), products_imprimantes = db.get_products_in_category('imprimantes'), products_stylo = db.get_products_in_category('stylos'))


@app.errorhandler(404)
def err404(error):
    """page manquante, erreur 404
    """
    return render_template('404.html', user_pseudo = getpseudo(), user_admin = getadminstate())

@app.route('/search/', methods=['POST'])
def search() :
    """page des résultats d'une recherche
    """
    content = request.form['search_bar']
    return render_template("recherche.html", search_title = content ,search_content = db.search(content))

@app.route('/panier/')
def panier():
    """page du panier
    """
    return render_template("panier.html", user_pseudo = getpseudo(), user_admin = getadminstate())


@app.route('/register/', methods=['POST', 'GET'])
def register():
    """page de l'enregistrement
    """
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
            user.isadmin = "NO"


            if passwordcheck.checkPassword((request.form["password"])) == True :
                user.password = generate_password_hash(request.form["password"], method='sha256', salt_length=8)
                user.add_user_in_database()
                mail.sendmail(user.email,"NONE",'notify_account_created')
            else : 
                flash("Mot de passe invalide", "error")
                return redirect(url_for('register'))
           
            # Connexion lors de l'enregistrement
            session["user"] = user.pseudo

            return render_template("register-successfully.html", user_pseudo = getpseudo(), user_admin = getadminstate())


@app.route('/login/', methods=['POST','GET'])
def login():
    """page de connexion
    """
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
                return render_template("pleasechangepassword.html", user_pseudo = getpseudo(), user_admin = getadminstate())
            else :
                return render_template("login-successfully.html", user_pseudo = getpseudo(), user_admin = getadminstate())

        else:
            flash("Identifiants incorrects, veuillez vérifier votre email et mot de passe.", "error") #Cas mot de passe incorrect.
            return redirect(url_for('login'))


@app.route('/logout/', methods=['GET'])
def logout():
    """action déconnection
    """
    try:
        session["user"]
        session.clear()
    except KeyError :
        return render_template("pleaseconnect.html")
    else:
        return render_template("logout-succesfully.html", user_pseudo = '', user_admin = getadminstate())


@app.route('/lostpassword/', methods=['POST', 'GET'])
def lost_password():
    """page de perte du mot de passe
    """
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
    """page de modification du mot de passe
    """
    user_ = db.get_user('pseudo', getpseudo())
    if passwordcheck.checkPassword((request.form["password"])) == True :
            user_.password = generate_password_hash(request.form["password"], method='sha256', salt_length=8)
            user_.modify_password_in_database()
            user_.set_temporary_password_state_no_in_database()
            mail.sendmail(user_.email,"NONE",'notify_update_password')
            return redirect(url_for('profil', user= user_, user_pseudo = getpseudo(), user_admin = getadminstate()))
    else :
        flash("Le mot de passe n'est pas valide !", "error")
        return redirect(url_for('profil', user=user_, user_pseudo = getpseudo(), user_admin = getadminstate()))


@app.route('/modify-personal-informations/', methods=['GET', 'POST'])
def modify_personal_informations():
    """page de modification des information personnelles
    """
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
            return render_template("account-succesfully-modified.html", user_pseudo = getpseudo(), user_admin = getadminstate())


@app.route('/deleteaccount/', methods=['GET','POST'])
def deleteaccount():
    """action de supprimer compte utilisateur
    """
    if request.method == 'GET' :
        return render_template('deleteaccount.html')
    else :
        user_ = db.get_user('pseudo', getpseudo())
        if request.form['delete-account'] == "Oui" :
            user_.delete_account_in_database()
            mail.sendmail(user_.email,"NONE",'notify_account_deleted')
            session.clear()
            return render_template("account-succesfully-deleted.html", user_pseudo = getpseudo(), user_admin = getadminstate())
        else :
            return redirect(url_for('profil', user=user_, user_pseudo = getpseudo(), user_admin = getadminstate()))


@app.route('/profil/', methods=['GET'])
def profil():
    """page du profil
    """
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

        return render_template("profil.html", user=user_ , user_pseudo = getpseudo(), user_admin = getadminstate())

@app.route('/<main_category>/')
def maincategory(main_category:str):
    """page d'une catégorie mère

    Args:
        main_category (str): catégorie en question
    """
    return render_template("main-category.html", category=main_category.capitalize(), categories = db.get_categories_in_main_category(main_category), user_pseudo = getpseudo(), user_admin = getadminstate())

@app.route('/<main_category>/<category>/')
def category(main_category:str, category:str):
    """page d'une sous catégorie

    Args:
        main_category (str): catégorie mère
        category (str): catégorie enfant
    """
    return render_template("category.html",main_cat = main_category, category=category.capitalize(), products=db.get_products_in_category(category), user_pseudo = getpseudo(), user_admin = getadminstate())


@app.route('/<main_category>/<category>/<product_id>/')
def product(main_category:str, category:str, product_id:int):
    """page d'un produit

    Args:
        main_category (str): catégorie mère
        category (str): catègorie enfant
        product_id (int): identifiant du produit
    """
    return render_template("product.html", product=db.get_product_by_id(product_id), user_pseudo = getpseudo(), user_admin = getadminstate())

### PARTIE UTILITAIRES ###
def getpseudo() -> str:
    """obtenir le pseudo de l'utilisateur actif

    Returns:
        str: pseudo de l'utilisateur
    """
    try :
        session["user"]
    except KeyError :
        user_session = ''
    else :
        user_ = db.get_user('pseudo', session['user'])
        user_session = user_.pseudo        
    return user_session

def getadminstate() -> bool:
    """savoir si l'utilisateur à les permission administrateur

    Returns:
        bool: vrai s'il est admin et faux à l'inverse
    """
    try :
        session["user"]
    except KeyError :
        return False
    user_ = db.get_user('pseudo', session['user'])
    if user_.isadmin == 'YES' :
        return True
    else :
        return False

def formatdateprofil() -> str:
    """modification du format de la date de naissance

    Returns:
        str: nouvelle date de naissance au format correct
    """
    user_ = db.get_user('pseudo', session['user'])
    birthdate = user_.datebirthday.split("-")
    new_birthday = birthdate[2] + '-' + birthdate[1] + '-' + birthdate[0]
    return new_birthday

def formatphoneprofil() -> str:
    """modification du format du numéro de téléphone

    Returns:
        str: numéro avec le bon format
    """
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
@app.route('/admin/', methods=['GET'])
def admin():
    """page principal administrateur (zone de connexion)
    """
    try:
        session["user"]
        if getadminstate() == True:
            return render_template('admin/general.html')
        else :
            raise KeyError
    except KeyError:
        return redirect(url_for('index', user_pseudo = getpseudo(), user_admin = getadminstate()))


@app.route('/admin/view-list/' ,methods = ['GET'])
def view_admin_list():
    """page de la liste des administrateur
    """
    try :
        session["user"]
        if getadminstate() == True:
            return render_template('admin/admin-view.html', users=db.get_admin_users())
        else :
            raise KeyError
    except KeyError:
        return redirect(url_for('index', user_pseudo = getpseudo(), user_admin = getadminstate()))


@app.route('/admin/modify-admin-list/ADD/', methods=['GET','POST'])
def add_admin() :
    """action d'ajout d'un administrateur
    """
    if request.method == 'GET' :    
        try :
            session["user"]
            if getadminstate() == True:
                return render_template('admin/modify-admin-list.html', state = 'ADD')
            else :
                raise KeyError
        except KeyError:
            return redirect(url_for('index', user_pseudo = getpseudo(), user_admin = getadminstate()))
    else :
        try :
            session["user"]
            user_ = db.get_user('pseudo', (request.form['pseudo']))
            if user_ != None :
                if getadminstate() == True:
                    user_.grant_admin_permissions()
                    return redirect(url_for('view_admin_list'))
                else :
                    raise KeyError
            else :
                return redirect(url_for('admin'))
        except KeyError:
            return redirect(url_for('index', user_pseudo = getpseudo(), user_admin = getadminstate()))


@app.route('/admin/modify-admin-list/DELETE/', methods=['GET','POST'])
def delete_admin() :
    """action de suppression d'un administrateur
    """
    if request.method == 'GET' :    
        try :
            session["user"]
            if getadminstate() == True:
                return render_template('admin/modify-admin-list.html', state='DELETE')
            else :
                raise KeyError
        except KeyError:
            return redirect(url_for('index', user_pseudo = getpseudo(), user_admin = getadminstate()))
    else :
        try :
            session["user"]
            user_ = db.get_user('pseudo', (request.form['pseudo']))
            if user_ != None :
                if getadminstate() == True:
                    user_.remove_admin_permissions()
                    return redirect(url_for('view_admin_list'))
                else :
                    raise KeyError
            else :
                return redirect(url_for('admin'))
        except KeyError:
            return redirect(url_for('index', user_pseudo = getpseudo(), user_admin = getadminstate()))


@app.route('/admin/produit/', methods=['POST', 'GET'])
def admin_view_product():
    """page de tous les produits
    """
    try:
        session["user"]
        if getadminstate() == True:
            return render_template('admin/product-view.html', products=db.get_table("Product"))
        else :
            raise KeyError
    except KeyError:
        return redirect(url_for('index', user_pseudo = getpseudo(), user_admin = getadminstate()))

@app.route('/admin/categorie/', methods=['POST', 'GET'])
def admin_view_category():
    """page de toutes les catégories
    """
    try:
        session["user"]
        if getadminstate() == True:
            return render_template('admin/category-view.html', cat=db.get_table("Category"))
        else :
            raise KeyError
    except KeyError:
        return redirect(url_for('index', user_pseudo = getpseudo(), user_admin = getadminstate()))


@app.route('/admin/produit/<product_id>/')
def admin_modify_product(product_id:int):
    """page de modification d'un produit

    Args:
        product_id (int): identifiant du produit
    """
    try:
        session["user"]
        if getadminstate() == True:
            return render_template('admin/product-modify.html', product=db.get_product_by_id(product_id))
        else :
            raise KeyError
    except KeyError:
        return redirect(url_for('index', user_pseudo = getpseudo(), user_admin = getadminstate()))


@app.route('/admin/produit/nouveau-produit/', methods=['POST', 'GET'])
def admin_new_product():
    """page d'jout d'un produit
    """
    try:        
        session["user"]
        if getadminstate() == True :
            return render_template('admin/product-append.html')
        else :
            raise KeyError
    except KeyError:
        return redirect(url_for('index', user_pseudo = getpseudo(), user_admin = getadminstate()))


@app.route('/admin/produit/nouveau-produit-request/', methods=['POST', 'GET'])
def admin_new_product_request():
    """action d'ajout d'un nouveau produit
    """
    if request.method == "POST":
        product = models.Product()
        product.name = request.form["name"]
        product.category = request.form["category"]
        product.price = float(request.form["price"])
        product.image = request.form["image"]
        product.description = request.form["description"]
        product.add_product_in_database()
        return redirect(url_for('admin_view_product'))
    else :
        pass

@app.route('/admin/produit/supprimer-produit/', methods=['POST', 'GET'])
def admin_delete_product():
    """page de suppresion d'un produit
    """
    try:        
        session["user"]
        if getadminstate() == True :
            if request.method == 'GET' :
                return render_template('admin/product-delete.html')
            else :
                identif = request.form['id']
                product = db.get_product_by_id(int(identif))
                if product != None :
                    product.delete_product_in_database()
                    return render_template('admin/product-view.html', products=db.get_table("Product"))
                else :
                    return render_template('admin/product-view.html', products=db.get_table("Product"))
        else :
            raise KeyError
    except KeyError:
        return redirect(url_for('index', user_pseudo = getpseudo(), user_admin = getadminstate()))

app.run(debug=True, port=app.config["PORT"], host=app.config["IP"]) 