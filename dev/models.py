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