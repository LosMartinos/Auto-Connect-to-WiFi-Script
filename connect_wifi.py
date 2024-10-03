import os
import subprocess
import time
from datetime import datetime

# Constants
WIFI_SSID = "YOURSSIDHERE" # change this to your network SSID
LOG_FILE = "wifi_log.txt"

# Check if already connected to any wifi
def is_connected_to_wifi():
    try:
        result = subprocess.check_output("netsh wlan show interfaces", shell=True, encoding='utf-8')
        return WIFI_SSID in result
    except subprocess.CalledProcessError as e:
        log_error(f"Error checking Wi-Fi status: {e}")
        return False

# Connect to Wi-Fi using the saved profile from windows
def connect_to_wifi():
    try:
        subprocess.check_output(f'netsh wlan connect name={WIFI_SSID}', shell=True, encoding='utf-8')
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

# Main
def main():
    # Check if already connected
    if not is_connected_to_wifi():
        # Attempt to connect using the saved profile from windows
        did_connect = connect_to_wifi()
    else:
        did_connect = False  # Already connected

    # Update logfile
    update_log(did_connect)
    # for debug purposes to not instantly close the popup cmd
    #input("Press Enter to exit...")

if __name__ == "__main__":
    main()
