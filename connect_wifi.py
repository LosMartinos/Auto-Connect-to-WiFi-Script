import os
import subprocess
import time

# Wi-Fi network name to connect
WIFI_SSID = "UPC-AP-5653080"
LOG_FILE = "wifi_log.txt"

def is_connected_to_wifi():
    try:
        # Run netsh command to check Wi-Fi status
        result = subprocess.check_output("netsh wlan show interfaces", shell=True, encoding='utf-8')
        return WIFI_SSID in result
    except subprocess.CalledProcessError:
        return False

def connect_to_wifi():
    try:
        # Attempt to connect to the specified Wi-Fi
        subprocess.check_output(f"netsh wlan connect name={WIFI_SSID}", shell=True, encoding='utf-8')
        return True
    except subprocess.CalledProcessError:
        return False

def update_log(did_connect):
    # Read current log counts from the log file, if it exists
    connected_count = 0
    already_connected_count = 0
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as log:
            try:
                lines = log.readlines()
                connected_count = int(lines[0].split(":")[1].strip())
                already_connected_count = int(lines[1].split(":")[1].strip())
            except (IndexError, ValueError):
                pass  # Handle malformed log files by resetting counts

    # Update the count based on whether we connected or found it already connected
    if did_connect:
        connected_count += 1
    else:
        already_connected_count += 1

    # Write updated counts back to the log file
    with open(LOG_FILE, 'w') as log:
        log.write(f"Connected to {WIFI_SSID} count: {connected_count}\n")
        log.write(f"Already connected count: {already_connected_count}\n")

def main():
    # Check if already connected to the desired Wi-Fi
    if not is_connected_to_wifi():
        did_connect = connect_to_wifi()
    else:
        did_connect = False  # No need to connect, already connected

    # Update the log based on whether we connected or not
    update_log(did_connect)

    # Wait for 2 seconds to let operations complete and exit
    time.sleep(2)

if __name__ == "__main__":
    main()
