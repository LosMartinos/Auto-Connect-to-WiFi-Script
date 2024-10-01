import os
import subprocess
import time
from cryptography.fernet import Fernet
import getpass
from datetime import datetime

# Constants
WIFI_SSID = "UPC-AP-5653080"
LOG_FILE = "wifi_log.txt"
PASSWORD_FILE = "wifi_password.enc"
KEY_FILE = "secret.key"

def load_or_generate_key():
    # Generate and save the key if it doesn't exist
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

def is_connected_to_wifi():
    try:
        result = subprocess.check_output("netsh wlan show interfaces", shell=True, encoding='utf-8')
        return WIFI_SSID in result
    except subprocess.CalledProcessError as e:
        log_error(f"Error checking Wi-Fi status: {e}")
        return False

def connect_to_wifi(password):
    try:
        # Setup the profile with password and connect using netsh
        profile_cmd = f'netsh wlan add profile filename="wifi_profile.xml"'
        subprocess.run(profile_cmd, shell=True, check=True)

        # Connect using the password
        result = subprocess.check_output(f'netsh wlan connect name={WIFI_SSID} keyMaterial={password}', shell=True, encoding='utf-8')
        return True
    except subprocess.CalledProcessError as e:
        log_error(f"Failed to connect to {WIFI_SSID}: {e}")
        return False

def log_error(message):
    with open(LOG_FILE, 'a') as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{timestamp} - {message}\n")

def update_log(did_connect):
    connected_count = 0
    already_connected_count = 0
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as log:
            try:
                lines = log.readlines()
                connected_count = int(lines[0].split(":")[1].strip())
                already_connected_count = int(lines[1].split(":")[1].strip())
            except (IndexError, ValueError):
                pass

    if did_connect:
        connected_count += 1
    else:
        already_connected_count += 1

    with open(LOG_FILE, 'w') as log:
        log.write(f"Connected to {WIFI_SSID} count: {connected_count}\n")
        log.write(f"Already connected count: {already_connected_count}\n")

def prompt_for_password():
    print("Enter Wi-Fi password for", WIFI_SSID)
    password = getpass.getpass(prompt="Password (input hidden): ")
    return password

def main():
    key = load_or_generate_key()
    
    # Check if already connected
    if not is_connected_to_wifi():
        password = decrypt_password(key)
        
        # If password is not available or incorrect, ask for password
        if not password:
            password = prompt_for_password()
            encrypt_password(password, key)
        
        did_connect = connect_to_wifi(password)
    else:
        did_connect = False  # Already connected

    # Update the log
    update_log(did_connect)

    time.sleep(2)

if __name__ == "__main__":
    main()
