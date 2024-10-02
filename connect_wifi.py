import os
import subprocess
import time
from cryptography.fernet import Fernet  # Import for decryption
from datetime import datetime

# Constants
WIFI_SSID = "UPC-AP-5653080"
LOG_FILE = "wifi_log.txt"
PASSWORD_FILE = "wifi_password.enc"
KEY_FILE = "secret.key"
BATCH_FILE = "connect_wifi.bat"

# Loads key for decryption
def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
        return key
    return None

# Decrypt password using key
def decrypt_password(key):
    f = Fernet(key)
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'rb') as pwd_file:
            encrypted_password = pwd_file.read()
        return f.decrypt(encrypted_password).decode()
    return None

# Check if already connected to any wifi
def is_connected_to_wifi():
    try:
        result = subprocess.check_output("netsh wlan show interfaces", shell=True, encoding='utf-8')
        return WIFI_SSID in result
    except subprocess.CalledProcessError as e:
        log_error(f"Error checking Wi-Fi status: {e}")
        return False

# Connect using the decrypted password 
def connect_to_wifi(password):
    try:
        subprocess.check_output(f'netsh wlan connect name={WIFI_SSID} keyMaterial={password}', shell=True, encoding='utf-8')
        return True
    except subprocess.CalledProcessError as e:
        log_error(f"Failed to connect to {WIFI_SSID}: {e}")
        return False

# Write errors to logfile
def log_error(message):
    with open(LOG_FILE, 'a') as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{timestamp} - {message}\n")

# Update counter in logfile to see how often the script was actually needed
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

# Run the change_password.py script to set the Wi-Fi password
def run_change_password_script():
    print("No saved Wi-Fi password found. Running password setup script...")
    subprocess.run(['python', 'change_password.py'], shell=True)
    print("Password setup complete. Please rerun the connect script.")

# Check if the password file exists
def main():
    if not os.path.exists(PASSWORD_FILE):
        run_change_password_script()
        return

    # Load the encryption key
    key = load_key()
    if not key:
        log_error("Encryption key not found. Please run the password setup.")
        return

    # Decrypt the password
    password = decrypt_password(key)
    if not password:
        log_error("Decryption failed. No valid password found.")
        return

    # Check if already connected
    if not is_connected_to_wifi():
        # Attempt to connect using the decrypted password
        did_connect = connect_to_wifi(password)
    else:
        did_connect = False  # Already connected

    # Update the log
    update_log(did_connect)

if __name__ == "__main__":
    main()
