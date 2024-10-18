
import curses
import argparse
from tools import check_tools_installed, enable_monitor_mode, disable_monitor_mode
from attacks import capture_handshake, crack_wpa_handshake, wps_attack, port_scan
from menu import draw_menu

def scan_networks(interface):
    """Scan for nearby Wi-Fi networks."""
    output = run_command(f"sudo airodump-ng {interface}mon")
    # You can add logic here to parse the output of airodump-ng and display it nicely.
    return output

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
