from cryptography.fernet import Fernet


# This function is used to decrypt the encrypted Two Factor Authenticator secret in the DB
def decrypt_secret(enc_key,data):
    fernet = Fernet(enc_key)
    decData = fernet.decrypt(data).decode()
    return decData
