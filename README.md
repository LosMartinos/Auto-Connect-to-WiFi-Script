# Auto Wi-Fi Connect Script

This project contains a Python script that automatically connects your Windows PC to a specific Wi-Fi network. The Wi-Fi password is assumed to be stored by Windows after a manual connection, eliminating the need for manual password input in the script.

## **Features**

- Automatically checks the Wi-Fi connection status.
- Automatically reconnects to the Wi-Fi network using a saved profile in Windows.
- Logs successful connections and errors (such as failed connection attempts).
- The script runs silently in the background.

## **Files**

### **1. `connect_wifi.py`**
This script performs the following tasks:
- Checks if the PC is connected to the specified Wi-Fi network.
- If not connected, it uses the Wi-Fi profile stored in Windows to connect.
- It logs all connection attempts and any errors that occur during the process.

## **How It Works**

- On **System Startup**: The script automatically runs at system startup (triggered via Task Scheduler or Startup Folder). It checks if the PC is connected to the Wi-Fi network and connects if necessary.
- On **Wi-Fi Disconnect Events**: Task Scheduler can be configured to trigger the script when a Wi-Fi disconnect event (Event ID 8001) is logged in the Windows Event Log. This ensures that the system reconnects if the Wi-Fi connection is dropped for any reason.
- **Wi-Fi Password Management**: Windows securely stores the Wi-Fi password **after the user connects manually** for the first time. The script then leverages this stored password for reconnection.

## **Setup Instructions**

### **Prerequisites**

- **Python**: You must have Python installed on your machine.
- **Wi-Fi Profile**: Ensure that you have manually connected to the Wi-Fi network at least once, so the profile is saved on your computer.

### **Task Scheduler**

1. Open Task Scheduler and create two new task.
2. Give the new task a name, e.g., "ConnectToWifiOnStartup" or "ConnectToWifiOnDisconnect".
3. Select **Run with highest privileges** and set it to **Run whether the user is logged on or not**.
4. Create a trigger on **Startup** and another trigger on **Event Log Microsoft-Windows-WLAN-AutoConfig/Operational** with **Source WLAN-AutoConfig** and **EventID 8001**.
5. Create an action and set the path to `pythonw.exe` as the program/script, and for the arguments, put the path to `connect_wifi.py`.

With these settings, the script will automatically connect your PC to Wi-Fi on startup and when a disconnect event is detected.

> **Note**: Disconnecting manually using Windows’ native Wi-Fi interface does not trigger Event 8001.

## **Why I Built This**

My PC frequently disconnects from the Wi-Fi for no apparent reason, and it's often not connected at startup. This solution automates the reconnection process, so I never have to manually click to connect to my home network again.