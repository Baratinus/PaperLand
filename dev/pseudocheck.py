import string

def checkPseudo(pseudo:str) -> bool:

    chrsNormaux = string.ascii_letters+string.digits
    nbChrsAnormaux = 0
    nbChrsNormaux = 0

    for letters in pseudo :
        if( letters not in chrsNormaux ) or letters == "'"  or letters == '"' or letters == ';':
            nbChrsAnormaux += 1
        else: 
            nbChrsNormaux += 1

    try:
        assert pseudo.find('SELECT') == 0
        assert pseudo.find('select') == 0
        assert pseudo.find('=') == 0
        assert nbChrsAnormaux == 0 
    except AssertionError :
        return False
    else :
        return True
    