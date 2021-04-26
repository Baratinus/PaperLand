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

    def __repr__(self):
        return "{} : {}".format(self.pseudo, self.email)


    def check_value(self, column:str, value:str) -> bool:
        if db.is_value_in_column("User", column, value):
            return True
        else:
            return False

    def add_user_in_database(self) :
        db.new_user(self)

    def modify_password_in_database(self) :
        db.update_user_password(self)

    def set_temporary_password_state_no_in_database(self) :
        db.set_user_temporary_password_state_no(self)

    def set_temporary_password_state_yes_in_database(self) :
        db.set_user_temporary_password_state_yes(self)

class Product:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.category = ""
        self.price = 0.0
        self.image = ""
        self.description = ""
