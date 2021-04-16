import string

def checkPassword(password:str) -> bool:

    chrsNormaux = string.ascii_letters+string.digits
    nbChrsAnormaux = 0
    nbChrsNormaux = 0
    nbMin = 0
    nbMaj = 0
    nbNbrs = 0
 
    for letters in password:
        #comprer les chrs qui ne sont ni lettre, ni chiffre
        if( letters not in chrsNormaux ):
            nbChrsAnormaux += 1
        else: #c'est une lettre ou un chiffre
            nbChrsNormaux += 1
        #compter le nb de maj
        if( 65 <= ord(letters) <= 90 ):
            nbMaj += 1
        #compter le nb de min
        if( 97 <= ord(letters) <= 122 ):
            nbMin += 1
        #compter les nbrs
        if( 48 <= ord(letters) <= 57 ):
            nbNbrs += 1

    try:
        assert nbMin >= 1
        assert nbMaj >= 1
        assert nbNbrs >= 1
    except AssertionError :
        return False
    else :
        return True
    