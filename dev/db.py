import sqlite3
import click

from flask import current_app, g
from flask.cli import with_appcontext

from . import models

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource(current_app.config['PATH'] + '/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    # new_user(pseudo="Baratinus", sexe="homme", email="p.baratinus@gmail.com", datebirthday="09/06/2003", password="azerty")

def gestion_db(function):
    """Décorateur pour éviter la répétiton de code
    """
    def function_decorator(*args):
        db = get_db()
        cur = db.cursor()
        f = function(*args, cursor=cur)
        # sauvegarder les changements
        db.commit()
        cur.close()
        return f
    return function_decorator

@gestion_db
def new_user(user:models.User, cursor:sqlite3.Cursor=None):
    """Ajout d'un nouvelle utilisateur dans la base de donnée

    Args:
        user (models.User): modèle de l'utilisateur
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.
    """
    cursor.execute(f"INSERT INTO User (pseudo,firstname,lastname,sexe,email,adress,city,postalcode,phone,datebirthday,password,temporarypassword,isadmin) VALUES ('{user.pseudo}','{user.firstname}','{user.lastname}','{user.sexe}','{user.email}','{user.adress}','{user.city}','{user.postalcode}','{user.phone}','{user.datebirthday}','{user.password}', '{user.temporarypassword}','{user.isadmin}')")
    
@gestion_db
def update_user_informations(user:models.User, cursor:sqlite3.Cursor=None):
    """mettre à jour les attributs de User dans la base de donnée

    Args:
        user (models.User): modeèle de l'utilisateur    
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.
    """
    cursor.execute(f"UPDATE User SET 'firstname'='{user.firstname}','lastname'='{user.lastname}','sexe'='{user.sexe}','email'='{user.email}','adress'='{user.adress}','city'='{user.city}','postalcode'='{user.postalcode}','phone'='{user.phone}','datebirthday'='{user.datebirthday}' WHERE pseudo='{user.pseudo}'")

@gestion_db
def update_user_password (user:models.User, cursor:sqlite3.Cursor=None):
    """mettre à jour le mot de passe de l'utilisateur   

    Args:
        user (models.User): modèle de l'utilisateur
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.
    """
    cursor.execute(f"UPDATE User SET password='{user.password}' WHERE pseudo='{user.pseudo}'")

@gestion_db
def delete_user(user:models.User, cursor:sqlite3.Cursor=None) :
    """supprimer un utilisateur grâce à son pseudo dans la bse de donnée

    Args:
        user (models.User): modèle de l'utilisateur
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.
    """
    cursor.execute(f"DELETE FROM User WHERE pseudo='{user.pseudo}'")

@gestion_db
def set_user_temporary_password_state_no (user:models.User, cursor:sqlite3.Cursor=None):
    """définir en actif le mot de passe temporaire dans la base de donnée

    Args:
        user (models.User): modèle de l'utilisateur
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.
    """
    cursor.execute(f"UPDATE User SET temporarypassword='NO' WHERE pseudo='{user.pseudo}'")

@gestion_db
def set_user_temporary_password_state_yes(user:models.User, cursor:sqlite3.Cursor=None):
    """définir en inactif le mot de passe temporaire dans la base de donnée

    Args:
        user (models.User): modèle de l'utilisateur
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.
    """
    cursor.execute(f"UPDATE User SET temporarypassword='YES' WHERE pseudo='{user.pseudo}'")

@gestion_db
def remove_admin_permission (user:models.User, cursor:sqlite3.Cursor=None):
    """retirer la permission d'administrateur à un utilisateur dans la base de donnée

    Args:
        user (models.User): modèle de l'utilisateur
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.
    """
    try :
        assert len(get_admin_users()) > 1
    except AssertionError :
        pass
    else :
        cursor.execute(f"UPDATE User SET isadmin='NO' WHERE pseudo='{user.pseudo}'")

@gestion_db
def grant_admin_permission(user:models.User, cursor:sqlite3.Cursor=None):
    """ajouter les permission d'aministrateur à un utilisateur

    Args:
        user (models.User): modèle de l'utilisateur
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.
    """
    cursor.execute(f"UPDATE User SET isadmin='YES' WHERE pseudo='{user.pseudo}'")

@gestion_db
def search(things:str, cursor:sqlite3.Cursor=None) -> tuple:
    """Chercher une chaine de caractère dans la base Product, sur ses attributs nom, catégorie et description

    Args:
        things (str): chaine de caractères à rechercher
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.

    Returns:
        tuple: tuple de produit trouvé
    """
    result = []
    for p in cursor.execute(f"SELECT produ.id,produ.name,produ.category,produ.price,produ.image,produ.description,cat.main_category FROM Product AS produ INNER JOIN Category AS cat ON (produ.category = cat.name) WHERE produ.name LIKE '%{things}%' OR produ.category LIKE '%{things}%' OR produ.description LIKE '%{things}%' LIMIT 15") :
        product = models.Product()
        product.id = p[0]
        product.name = p[1]
        product.category = p[2]
        product.price = p[3]
        product.image = p[4]
        product.description = p[5]
        product.main_cat = p[6]
        result.append(product)
    return tuple(result)


@gestion_db
def get_user(column:str, value:str, cursor:sqlite3.Cursor=None) -> models.User:
    """obtenir les informations d'un utilisateur en fonction de l'email

    Args:
        column (str): non de la colonne (vf schema.sql), attention mettre une colonne à valeur UNIQUE
        value (str): valeur de la colonne respective
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.

    Returns:
        models.User: utilisateur, si aucun utilisateur existe renvoie None
    """
    cursor.execute(f"SELECT * FROM User WHERE {column}='{value}'")
    try:
        param = cursor.fetchall()[0]
        user = models.User()
        user.pseudo = param[0]
        user.firstname = param[1]
        user.lastname = param[2]
        user.sexe = param[3]
        user.email = param[4]
        user.adress = param[5]
        user.city = param[6]
        user.postalcode = param[7]
        user.phone = param[8]
        user.datebirthday = param[9]
        user.password = param[10]
        user.temporarypassword = param[11]
        user.isadmin = param[12]
        return user
    except:
        return None

@gestion_db
def is_value_in_column(table:str, column:str, value:str, cursor:sqlite3.Cursor=None) -> bool:
    """chercher si une valeur est dans une colonne d'une table

    Args:
        table (str): table en question
        column (str): colonne où chercher
        value (str): valeur à rechercher
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.

    Returns:
        bool: vrai si la valeur est trouvé et faux à l'inverse
    """
    cursor.execute(f"SELECT {column} FROM {table} WHERE {column}='{value}'")
    a = len(cursor.fetchall())
    return(a != 0)

@gestion_db
def get_admin_users(cursor:sqlite3.Cursor=None) -> list:
    """Obtenir tous les administrateur 

    Args:
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.

    Returns:
        list: liste des administrateur
    """     
    results = []
    for user in cursor.execute(f"SELECT pseudo FROM User WHERE isadmin='YES'") :
        results.append(list(user))
    return results

@gestion_db
def get_categories_in_main_category(main_category:str, cursor:sqlite3.Cursor=None) -> tuple :
    """Obtenir les sous catégories d'une catégorie mère

    Args:
        main_category (str): catégorie mère
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.

    Returns:
        tuple: tuple des catégories enfants
    """
    result = []
    for p in cursor.execute(f"SELECT * FROM category WHERE main_category='{main_category}'"):
        category = models.Category()
        category.name = p[0]
        category.main_category = p[1]
        result.append(p)
    return tuple(result)

@gestion_db
def get_products_in_category(category:str, cursor:sqlite3.Cursor=None) -> tuple:
    """Obtenir les produits d'une catégorie

    Args:
        category (str): catégorie
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.

    Returns:
        tuple: tuple des produits
    """
    result = []
    for p in cursor.execute(f"SELECT * FROM product WHERE category='{category}'"):
        product = models.Product()
        product.id = p[0]
        product.name = p[1]
        product.category = p[2]
        product.price = p[3]
        product.image = p[4]
        product.description = p[5]
        result.append(product)
    return tuple(result)

@gestion_db
def get_category_by_name(name:str, cursor:sqlite3.Cursor=None) -> models.Category:
    """Obtenir une catégorie grâce à son nom

    Args:
        name (str): nom de la catégorie
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.

    Returns:
        models.Category: catégorie
    """
    for p in cursor.execute(f"SELECT * FROM Category WHERE name='{name}'"):
        categorie = models.Category()
        categorie.name = p[0]
        categorie.main_category = p[1]
        return categorie

@gestion_db
def new_category(category:models.Category, cursor:sqlite3.Cursor=None) -> None:
    """Inscrir une nouvelle catégorie dans la base de donnée

    Args:
        category (models.Category): modèle d'une catégorie
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.
    """
    cursor.execute(f'INSERT INTO Category (name,main_category) VALUES ("{category.name}","{category.main_category}")')

@gestion_db
def delete_category(category:models.Category, cursor:sqlite3.Cursor=None) -> None:
    cursor.execute(f"DELETE FROM Category WHERE name='{category.name}'")

@gestion_db
def get_product_by_id(id:int, cursor:sqlite3.Cursor=None):
    """Obtenir un produit grâce à son identifiant

    Args:
        id (int): indetifiant
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.

    Returns:
        models.Product: produit
    """ 
    for p in cursor.execute(f"SELECT * FROM product WHERE id='{str(id)}'"):
        product = models.Product()
        product.id = p[0]
        product.name = p[1]
        product.category = p[2]
        product.price = p[3]
        product.image = p[4]
        product.description = p[5]
        return product

@gestion_db
def get_table(table:str, cursor:sqlite3.Cursor=None) -> tuple:
    """Obtenir l'intégralité d'une table

    Args:
        table (str): table
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.

    Returns:
        tuple: tuple de chaque ligne de la table
    """
    result = []
    for p in cursor.execute(f"SELECT * FROM {table}"):
        result.append(tuple([e for e in p]))
    return tuple(result)

@gestion_db
def new_product(product:models.Product, cursor:sqlite3.Cursor=None) -> None:
    """Inscrire un nouveau produit dans la base de donnée

    Args:
        product (models.Product): modèle d'un produit
        cursor (sqlite3.Cursor, optional): ne pas remplir. Defaults to None.
    """
    cursor.execute(f'INSERT INTO Product (name,category,price,image,description) VALUES ("{product.name}","{product.category}",{product.price},"{product.image}","{product.description}")')

@gestion_db
def update_product_informations(product:models.Product, cursor:sqlite3.Cursor=None) -> None:
    cursor.execute(f"UPDATE Product SET name='{product.name}',category='{product.category}',price='{product.price}',description='{product.description}' WHERE id='{product.id}'")

@gestion_db
def delete_product(product:models.Product, cursor:sqlite3.Cursor=None) -> None:
    """supprimer un produit de la base de donnée

    Args:
        product (models.Product): modèle d'un produit
        cursor (sqlite3.Cursor, optional): ne pas replir. Defaults to None.
    """
    cursor.execute(f"DELETE FROM Product WHERE name='{product.name}'")

@gestion_db
def add_product_to_cart(user:models.User, product:models.Product, quantity: int, cursor:sqlite3.Cursor=None) -> None :
    cursor.execute(f"INSERT INTO Cart (user, product, quantity) VALUES ({user.pseudo},{product.id},{quantity})")
