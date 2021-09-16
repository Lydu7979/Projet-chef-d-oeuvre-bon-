import hashlib

def mod(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def verif(password,veri_text):
    if mod(password) == veri_text:
        return veri_text
	return False