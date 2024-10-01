import os
import subprocess
import time

# wifi network name to connect
WIFI_SSID = "UPC-AP-5653080"
LOG_FILE = "wifi_log.txt"
PASSWORD_FILE = "wifi_password.enc"
KEY_FILE = "secret.key"
RETRY_INTERVAL = 10  # Retry every 10 seconds
MAX_RETRIES = 6      # Retry for up to 1 minute (6 retries)

def is_connected_to_wifi():
    try:
        # run netsh command to check wifi status
        result = subprocess.check_output("netsh wlan show interfaces", shell=True, encoding='utf-8')
        return WIFI_SSID in result
    except subprocess.CalledProcessError:
        return False

def connect_to_wifi():
    try:
        # attempt to connect to the wifi
        subprocess.check_output(f"netsh wlan connect name={WIFI_SSID}", shell=True, encoding='utf-8')
        return True
    except subprocess.CalledProcessError:
        return False

def log_error(message):
    with open(LOG_FILE, 'a') as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{timestamp} - {message}\n")

def update_log(did_connect):
    # read current log counts from the log file, if it exists
    connected_count = 0
    already_connected_count = 0
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as log:
            try:
                lines = log.readlines()
                connected_count = int(lines[0].split(":")[1].strip())
                already_connected_count = int(lines[1].split(":")[1].strip())
            except (IndexError, ValueError):
                pass  # if log files are not readable reset by resetting counts

    # update the count 
    # this counter is purely for my own entertainment on how buggy my pc is
    if did_connect:
        connected_count += 1
    else:
        already_connected_count += 1

    # write updated counts to logfile
    with open(LOG_FILE, 'w') as log:
        log.write(f"Connected to {WIFI_SSID} count: {connected_count}\n")
        log.write(f"Already connected count: {already_connected_count}\n")

def main():
    # check if script needs to connect
    if not is_connected_to_wifi():
        did_connect = connect_to_wifi()
    else:
        did_connect = False 

    # Update the log 
    update_log(did_connect)

if __name__ == "__main__":
    main()
