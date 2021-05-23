from . import db

class User:
    """modèle d'un utilisateur
    """
    def __init__(self):
        self.pseudo = ""
        self.firstname = ""
        self.lastname = ""
        self.sexe = ""
        self.email = ""
        self.adress = ""
        self.city = ""
        self.postalcode = ""
        self.phone = ""
        self.datebirthday = ""
        self.password = ""
        self.temporarypassword = ""
        self.isadmin = ""

    def __repr__(self):
        return "{} : {}".format(self.pseudo, self.email)

    def check_value(self, column:str, value:str) -> bool:
        """savoir si une valeur précise est dans la base de donnée

        Args:
            column (str): colonne où rechercher 
            value (str): valeur à rechercher

        Returns:
            bool: vrai si valeur trouvé et faux si non trouvé
        """
        if db.is_value_in_column("User", column, value):
            return True
        else:
            return False

    def add_user_in_database(self) :
        """ajout l'utilisateur à la base de donnée
        """
        db.new_user(self)

    def modify_personal_informations_in_database(self) :
        """mettre à jour l'utilisateur dans la base de donnée
        """
        db.update_user_informations(self)

    def delete_account_in_database(self) :
        """supprimer l'utilisateur de la base de donnée
        """
        db.delete_user(self)

    def modify_password_in_database(self) :
        """mettre à jour l'utilisateur dans la base de donnée
        """
        db.update_user_password(self)

    def set_temporary_password_state_no_in_database(self) :
        """définir en inactif le mot de passe temporaire dans la base de donnée
        """
        db.set_user_temporary_password_state_no(self)

    def set_temporary_password_state_yes_in_database(self) :
        """définir en actif le mot de passe temporaire dans la base de donnée
        """
        db.set_user_temporary_password_state_yes(self)

    def remove_admin_permissions(self) :
        """supprimer les permissions administrateur à un utilisateur dans la base de donnée
        """
        db.remove_admin_permission(self)

    def grant_admin_permissions(self) :
        """définir l'utilsiateur comme administrateur dans la base de donnée
        """
        db.grant_admin_permission(self)

class Product:
    """modèle d'un produit
    """
    def __init__(self):
        self.id = 0
        self.name = ""
        self.category = ""
        self.price = 0.0
        self.image = ""
        self.description = ""
        self.main_cat = ""
    
    def check_value(self, column:str, value:str) -> bool:
        """savoir si une valeur précise est dans la base de donnée

        Args:
            column (str): colonne où rechercher 
            value (str): valeur à rechercher

        Returns:
            bool: vrai si valeur trouvé et faux si non trouvé
        """
        if db.is_value_in_column("Product", column, value):
            return True
        else:
            return False
    def check_category(self) -> bool:
        if db.is_value_in_column("Category", "name", self.category):
            return True
        else:
            return False
    def modify_product_in_database(self) :
        db.update_product_informations(self)

    def add_product_in_database(self):
        """ajouter le produit dans la base de donnée
        """
        db.new_product(self)
    
    def delete_product_in_database(self) :
        """supprimer le produit de la base de donnée
        """
        db.delete_product(self)

class Category:
    """modèle d'une catégorie
    """
    def __init__(self):
        self.name = ""
        self.main_category = ""

    def check_main(self) -> bool:
        if db.is_value_in_column("Main_categories", "name", self.main_category):
            return True
        else:
            return False

    def add_category_in_database(self):
        """ajouter la catégorie dans la base de donnée
        """
        db.new_category(self)

    def delete_category_in_database(self) :
        db.delete_category(self)
