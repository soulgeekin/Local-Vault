from cryptography.fernet import Fernet
import os
import json
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64


def load_vault():
    if os.path.exists('vault.json'):
        with open ('vault.json' ,'r') as file:
            return json.load(file)
    else:
       return {}

def save_vault(data):
    with open('vault.json', 'w') as file:
        json.dump(data, file)

def add_password(site,password,key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode()).decode()
    data = load_vault()
    data[site] = encrypted_password
    save_vault(data)
    print('Saved Password!')

def get_password(site,key):
    fernet = Fernet(key)
    data = load_vault()
    if site in data:
        encrypted = data[site]
        decrypted = fernet.decrypt(encrypted.encode()).decode()
        return decrypted
    else:
        print('Invalid site. Are you sure you added the site password before?')
        return None

# master pass functions
def is_first_launch():
     if os.path.exists('master.hash'):
        return False
     else:
        return True


def derive_key(password, salt):
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
    backend=default_backend()
)
    raw_key = kdf.derive(password.encode())
    key = base64.urlsafe_b64encode(raw_key)
    return key
    

    



def create_master_password(password):
    salt = os.urandom(16)
    hashed_pass = hashlib.sha256(salt + password.encode()).hexdigest()
    with open('master.hash', 'wb') as file:
        file.write(salt)
        file.write(hashed_pass.encode())

def check_master_password(password):
    with open('master.hash', 'rb') as file:
        salt = file.read(16)
        stored_hash = file.read().decode()
    attempted_hash = hashlib.sha256(salt + password.encode()).hexdigest()
    return attempted_hash == stored_hash, salt