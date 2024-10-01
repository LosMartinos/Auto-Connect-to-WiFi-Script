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
RETRY_INTERVAL = 10  # Retry every 10 seconds
MAX_RETRIES = 6      # Retry for up to 1 minute (6 retries)
BATCH_FILE = "connect_wifi.bat"  # The batch file to modify

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
        # Connect using the password
        subprocess.check_output(f'netsh wlan connect name={WIFI_SSID} keyMaterial={password}', shell=True, encoding='utf-8')
        return True
    except subprocess.CalledProcessError as e:
        log_error(f"Failed to connect to {WIFI_SSID}: {e}")
        return False

def retry_connection(password):
    retries = 0
    while retries < MAX_RETRIES:
        if connect_to_wifi(password):
            return True
        retries += 1
        time.sleep(RETRY_INTERVAL)  # Wait before retrying
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

def update_batch_file_to_pythonw():
    # Read the batch file content and replace "python" with "pythonw"
    with open(BATCH_FILE, 'r') as file:
        content = file.read()

    if "pythonw" not in content:  # Only replace if it's not already using pythonw
        new_content = content.replace("python", "pythonw")
        with open(BATCH_FILE, 'w') as file:
            file.write(new_content)
        log_error("Batch file updated to use pythonw for silent execution.")

def main():
    key = load_or_generate_key()

    # Check if already connected
    if not is_connected_to_wifi():
        password = decrypt_password(key)
        
        # If password is not available, prompt user to enter it
        if not password:
            password = prompt_for_password()
            encrypt_password(password, key)
            update_batch_file_to_pythonw()  # Modify batch file to use pythonw for future runs

        # Retry to connect for up to 1 minute
        did_connect = retry_connection(password)
    else:
        did_connect = False  # Already connected

    # Update the log
    update_log(did_connect)

    time.sleep(2)

if __name__ == "__main__":
    main()
