import hashlib

def modi(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def verif(password,veri_text):
    if modi(password) == veri_text:
        return veri_text
    
    return False