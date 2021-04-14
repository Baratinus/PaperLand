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

    def __repr__(self):
        return "{} : {}".format(self.pseudo, self.email)


    def check_value(self, column:str, value:str) -> bool:
        if db.is_value_in_column("User", column, value):
            return True
        else:
            return False

    def add_user_in_database(self):
        db.new_user(self)

    # # TESTS de fonctions ( a enlever si ça pose pb ou si qqn veut le faire en + propre) :  BUG FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME 

    # def check_birthday(self, value:str) -> bool: BUG
    #     if db.is_value_in_column("User", "datebirthday", value):
    #         return True
    #     else:
    #         return False

    # def get_password(self, email:str, birthday:str) -> str :
    #     return db.search_password_e_db(email,birthday) BUG
        
    # def check_email(self, value:str) -> bool: BUG
    #     if db.is_value_in_column("User", "email", value) :
    #         return True
    #     else:
    #         return False

    # def check_pseudo(self,value:str) -> bool: BUG
    #     if db.is_value_in_column("User", "pseudo", value):
    #         return True
    #     else:
    #         return False FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME 