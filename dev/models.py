from . import db

class User:
    def __init__(self):
        self.__pseudo = ""
        self.firstname = ""
        self.lastname = ""
        self.sexe = ""
        self.__email = ""
        self.adress = ""
        self.city = ""
        self.postalcode = ""
        self.phone = ""
        self.datebirthday = ""
        self.password = ""


    def get_email(self) -> str:
        return self.__email
    def set_email(self, value:str) -> None:
        # vérification si l'email n'est pas déjà présente
        if not db.is_value_in_column("User", "email", value):
            self.__email = value
        else:
            raise ValueError("L'email est déjà présente dans la base de données")
    email = property(get_email, set_email)


    def get_pseudo(self) -> str:
        return self.__pseudo

    def set_pseudo(self, value:str) -> None:
        # vérification si le pseudo n'est pas déjà présente
        if not db.is_value_in_column("User", "pseudo", value):
            self.__pseudo = value
        else:
            raise ValueError("Pseudo déjà présent dans la base de données")
    pseudo = property(get_pseudo, set_pseudo)

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