from . import db

class User:
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
        if db.is_value_in_column("User", column, value):
            return True
        else:
            return False

    def add_user_in_database(self) :
        db.new_user(self)

    def modify_personal_informations_in_database(self) :
        db.update_user_informations(self)

    def delete_account_in_database(self) :
        db.delete_user(self)

    def modify_password_in_database(self) :
        db.update_user_password(self)

    def set_temporary_password_state_no_in_database(self) :
        db.set_user_temporary_password_state_no(self)

    def set_temporary_password_state_yes_in_database(self) :
        db.set_user_temporary_password_state_yes(self)

    def remove_admin_permissions(self) :
        db.remove_admin_permission(self)

    def grant_admin_permissions(self) :
        db.grant_admin_permission(self)

class Product:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.category = ""
        self.price = 0.0
        self.image = ""
        self.description = ""
        self.main_cat = ""
    
    def check_value(self, column:str, value:str) -> bool:
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
        db.new_product(self)
    
    def delete_product_in_database(self) :
        db.delete_product(self)

class Category:
    def __init__(self):
        self.name = ""
        self.main_category = ""

    def check_main(self) -> bool:
        if db.is_value_in_column("Main_categories", "name", self.main_category):
            return True
        else:
            return False

    def add_category_in_database(self):
        db.new_category(self)

    def delete_category_in_database(self) :
        db.delete_category(self)
