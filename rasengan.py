
import curses
import curses.textpad
import argparse
import sys
from tools import check_tools_installed, enable_monitor_mode, disable_monitor_mode, run_command
from attacks import capture_handshake, crack_wpa_handshake, wps_attack, port_scan
from menu import draw_menu
import re

def find_wireless_interface():
    # Find the wireless interface (e.g., wlan0).
    output = run_command("iwconfig")
    for line in output.splitlines():
        if "IEEE 802.11" in line:
            return line.split()[0]  # Extract the interface name
    return None

def scan_networks(interface):
    # Scan for nearby Wi-Fi networks and parse the results.
    output = run_command(f"sudo airodump-ng {interface}mon")

    # Parse the output for network details (BSSID, Channel, ESSID)
    networks = []
    network_re = re.compile(r'([0-9A-F:]{17})\s+\d+\s+(\d+)\s+-\d+\s+-\d+\s+\d+\s+\S+\s+(.+)')
    
    for line in output.splitlines():
        match = network_re.search(line)
        if match:
            bssid, channel, essid = match.groups()
            networks.append((bssid, channel, essid.strip()))
    
    return networks

def display_network_list(stdscr, networks):
    # Display a list of networks and allow the user to select one.
    selected = 0
    while True:
        stdscr.clear()
        stdscr.border(0)
        stdscr.addstr(1, 2, "Select a Network", curses.A_BOLD)
        
        # Display networks
        for i, network in enumerate(networks):
            bssid, channel, essid = network
            if i == selected:
                stdscr.addstr(i + 3, 2, f"{essid} (BSSID: {bssid}, Channel: {channel})", curses.A_REVERSE)
            else:
                stdscr.addstr(i + 3, 2, f"{essid} (BSSID: {bssid}, Channel: {channel})")
        
        stdscr.refresh()

        key = stdscr.getch()

        # Navigate with arrow keys
        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(networks) - 1:
            selected += 1
        elif key == ord('
'):  # Enter key
            return networks[selected]
        elif key == 27:  # Escape key to cancel
            return None

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(0)
    
    # Automatically detect the wireless interface
    interface = find_wireless_interface()
    if not interface:
        stdscr.addstr(10, 2, "No wireless interface found. Please check your setup.")
        stdscr.getch()
        sys.exit(1)
    
    tools_status = check_tools_installed()
    if "missing" in tools_status:
        stdscr.addstr(12, 2, tools_status)
        stdscr.getch()
        sys.exit(1)

    # Enable mouse events and key events
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    stdscr.keypad(True)

    while True:
        draw_menu(stdscr)
        choice = stdscr.getch()

        if choice == curses.KEY_MOUSE:
            try:
                _, mx, my, _, _ = curses.getmouse()  # Get mouse position
                if my == 3:  # Clicked on "Scan for Networks"
                    choice = ord('1')
                elif my == 4:  # Clicked on "Capture WPA Handshake"
                    choice = ord('2')
                elif my == 5:  # Clicked on "Crack WPA Password"
                    choice = ord('3')
                elif my == 6:  # Clicked on "WPS Attack"
                    choice = ord('4')
                elif my == 7:  # Clicked on "Port Scan"
                    choice = ord('5')
                elif my == 8:  # Clicked on "Exit"
                    choice = ord('6')
            except curses.error:
                pass

        # Handle keyboard inputs
        if choice == ord('1'):  # Scan for Networks
            enable_monitor_mode(interface)
            stdscr.addstr(10, 2, "Scanning for networks...")
            stdscr.refresh()

            networks = scan_networks(interface)
            disable_monitor_mode(interface)

            if networks:
                selected_network = display_network_list(stdscr, networks)
                stdscr.addstr(12, 2, f"Selected Network: {selected_network[2]} (BSSID: {selected_network[0]})")
            else:
                stdscr.addstr(12, 2, "No networks found.")
            stdscr.getch()

        elif choice == ord('2'):  # Capture WPA Handshake
            # Automatically proceed with selected network
            stdscr.addstr(10, 2, f"Capturing handshake for {selected_network[2]} (BSSID: {selected_network[0]})")
            curses.echo()
            bssid = selected_network[0]
            channel = selected_network[1]
            enable_monitor_mode(interface)
            output = capture_handshake(bssid, channel, interface)
            disable_monitor_mode(interface)
            stdscr.addstr(15, 2, output)
            stdscr.getch()

        elif choice == ord('3'):  # Crack WPA Password
            stdscr.addstr(10, 2, "Enter path to wordlist: ")
            wordlist = stdscr.getstr(11, 2, 50).decode()
            bssid = selected_network[0]
            output = crack_wpa_handshake(wordlist, bssid)
            stdscr.addstr(15, 2, output)
            stdscr.getch()

        elif choice == ord('4'):  # WPS Attack
            stdscr.addstr(10, 2, f"Running WPS attack on {selected_network[2]} (BSSID: {selected_network[0]})")
            bssid = selected_network[0]
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
    args = parser.parse_args()
    curses.wrapper(main)
