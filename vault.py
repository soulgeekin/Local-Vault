from cryptography.fernet import Fernet
import os
import json
import hashlib


if os.path.exists('key.key'):
    with open('key.key',  'rb') as file:
        key = file.read()
else:
    key = Fernet.generate_key()
    with open('key.key', 'wb') as file:
        file.write(key)

def load_vault():
    if os.path.exists('vault.json'):
        with open ('vault.json' ,'r') as file:
            return json.load(file)
    else:
       return {}

def save_vault(data):
    with open('vault.json', 'w') as file:
        json.dump(data, file)

def add_password(site , password):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode()).decode()
    data = load_vault()
    data[site] = encrypted_password
    save_vault(data)
    print('Saved Password!')

def get_password(site):
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
    return attempted_hash == stored_hash