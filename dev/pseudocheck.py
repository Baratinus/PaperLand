import string

def checkPseudo(pseudo:str) -> bool:
    '''
        Fonction permettant de vérifier si un pseudo Utilisateur ne contient pas d'injection SQL ou de caractères interdit ( ' / ; / " / = ).
    '''
    chrsNormaux = string.ascii_letters+string.digits
    nbChrsAnormaux = 0
    nbChrsNormaux = 0

    for letters in pseudo :
        if letters not in chrsNormaux or letters == "'"  or letters == '"' or letters == ';':
            nbChrsAnormaux += 1
        else: 
            nbChrsNormaux += 1
    
    try:
        assert pseudo.find('SELECT') == -1
        assert pseudo.find('select') == -1
        assert pseudo.find('=') == -1
        assert nbChrsAnormaux == 0
    except AssertionError :
        return False
    else :
        return True
    
if __name__ == "__main__":
    print(checkPseudo("OUI"))