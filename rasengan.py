import curses
import subprocess
import shutil
import sys
import argparse

REQUIRED_TOOLS = ["airmon-ng", "airodump-ng", "aircrack-ng", "reaver", "nmap"]

def check_tools_installed():
    """Check if all required tools are installed."""
    missing_tools = []
    for tool in REQUIRED_TOOLS:
        if not shutil.which(tool):
            missing_tools.append(tool)
    
    if missing_tools:
        return f"The following tools are missing: {', '.join(missing_tools)}. Please install them."
    return "All required tools are installed."

def run_command(command):
    """Function to run system commands and handle errors."""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.decode()}"

def enable_monitor_mode(interface):
    """Enable monitor mode on Wi-Fi adapter."""
    return run_command(f"sudo airmon-ng start {interface}")

def scan_networks(interface):
    """Scan for nearby Wi-Fi networks."""
    return run_command(f"sudo airodump-ng {interface}mon")

def capture_handshake(bssid, channel, interface):
    """Capture WPA/WPA2 handshake."""
    return run_command(f"sudo airodump-ng --bssid {bssid} --channel {channel} -w capture {interface}mon")

def crack_wpa_handshake(wordlist, bssid):
    """Attempt to crack WPA/WPA2 password using a captured handshake."""
    return run_command(f"sudo aircrack-ng -w {wordlist} -b {bssid} capture-01.cap")

def wps_attack(bssid, interface):
    """Attempt to crack WPS using Reaver."""
    return run_command(f"sudo reaver -i {interface}mon -b {bssid} -vv")

def port_scan(ip):
    """Scan for open ports on a router."""
    return run_command(f"sudo nmap -Pn -sS -p- {ip}")

def disable_monitor_mode(interface):
    """Disable monitor mode after use."""
    return run_command(f"sudo airmon-ng stop {interface}mon")

def draw_menu(stdscr):
    stdscr.clear()
    stdscr.border(0)
    stdscr.addstr(1, 2, "Rasengan: Wi-Fi Security Checker", curses.A_BOLD)
    stdscr.addstr(3, 2, "[1] Scan for Networks")
    stdscr.addstr(4, 2, "[2] Capture WPA Handshake")
    stdscr.addstr(5, 2, "[3] Crack WPA Password")
    stdscr.addstr(6, 2, "[4] WPS Attack")
    stdscr.addstr(7, 2, "[5] Port Scan")
    stdscr.addstr(8, 2, "[6] Exit")
    stdscr.addstr(10, 2, "Choose an option: ")
    stdscr.addstr(14, 2, "Created by: Chararch | GitHub: https://github.com/chararch", curses.A_DIM)

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(0)
    
    interface = "wlan0"
    tools_status = check_tools_installed()
    if "missing" in tools_status:
        stdscr.addstr(12, 2, tools_status)
        stdscr.getch()
        sys.exit(1)

    while True:
        draw_menu(stdscr)
        choice = stdscr.getch()
        stdscr.clear()

        if choice == ord('1'):  # Scan for Networks
            enable_monitor_mode(interface)
            stdscr.addstr(10, 2, "Scanning for networks...")
            output = scan_networks(interface)
            disable_monitor_mode(interface)
            stdscr.addstr(12, 2, output)
            stdscr.getch()

        elif choice == ord('2'):  # Capture WPA Handshake
            stdscr.addstr(10, 2, "Enter BSSID: ")
            curses.echo()
            bssid = stdscr.getstr(11, 2, 20).decode()
            stdscr.addstr(12, 2, "Enter Channel: ")
            channel = stdscr.getstr(13, 2, 5).decode()
            enable_monitor_mode(interface)
            output = capture_handshake(bssid, channel, interface)
            disable_monitor_mode(interface)
            stdscr.addstr(15, 2, output)
            stdscr.getch()

        elif choice == ord('3'):  # Crack WPA Password
            stdscr.addstr(10, 2, "Enter path to wordlist: ")
            wordlist = stdscr.getstr(11, 2, 50).decode()
            stdscr.addstr(12, 2, "Enter BSSID: ")
            bssid = stdscr.getstr(13, 2, 20).decode()
            output = crack_wpa_handshake(wordlist, bssid)
            stdscr.addstr(15, 2, output)
            stdscr.getch()

        elif choice == ord('4'):  # WPS Attack
            stdscr.addstr(10, 2, "Enter BSSID: ")
            curses.echo()
            bssid = stdscr.getstr(11, 2, 20).decode()
            enable_monitor_mode(interface)
            output = wps_attack(bssid, interface)
            disable_monitor_mode(interface)
            stdscr.addstr(15, 2, output)
            stdscr.getch()

        elif choice == ord('5'):  # Port Scan
            stdscr.addstr(10, 2, "Enter IP of the router: ")
            ip = stdscr.getstr(11, 2, 20).decode()
            output = port_scan(ip)
            stdscr.addstr(13, 2, output)
            stdscr.getch()

        elif choice == ord('6'):  # Exit
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rasengan: Wi-Fi Security Checker")
    parser.add_argument("--help", action="help", help="Show this help message and exit")
    
    args = parser.parse_args()

    curses.wrapper(main)