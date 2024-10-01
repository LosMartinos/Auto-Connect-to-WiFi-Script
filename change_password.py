import os
import getpass
from cryptography.fernet import Fernet

PASSWORD_FILE = "wifi_password.enc"
KEY_FILE = "secret.key"

def load_or_generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
    return key

def encrypt_password(password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    with open(PASSWORD_FILE, 'wb') as pwd_file:
        pwd_file.write(encrypted_password)

def decrypt_password(key):
    f = Fernet(key)
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'rb') as pwd_file:
            encrypted_password = pwd_file.read()
        return f.decrypt(encrypted_password).decode()
    return None

def change_password():
    key = load_or_generate_key()
    
    # Prompt user for new password
    print("Enter Wi-Fi password for UPC-AP-5653080:")
    new_password = getpass.getpass(prompt="Password (input hidden): ")

    # Encrypt and save the new password
    encrypt_password(new_password, key)
    print("Password updated and saved successfully.")

if __name__ == "__main__":
    change_password()
