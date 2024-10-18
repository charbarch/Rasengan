import curses
import curses.textpad
import argparse
import sys
import re
import shutil
import subprocess
import logging
from tools import check_tools_installed, enable_monitor_mode, disable_monitor_mode, run_command
from attacks import capture_handshake, crack_wpa_handshake, wps_attack, port_scan
from menu import draw_menu

def check_dependencies():
    """
    Check if the required tools are installed on the system.
    """
    required_tools = ["airmon-ng", "airodump-ng", "aireplay-ng", "reaver"]
    missing_tools = []
    
    for tool in required_tools:
        if not shutil.which(tool):
            missing_tools.append(tool)
    
    if missing_tools:
        return f"Missing tools: {', '.join(missing_tools)}. Please install the missing tools and try again."
    return ""

def find_wireless_interface():
    """
    Find the wireless interface (e.g., wlan0).
    """
    output = run_command("iwconfig")
    for line in output.splitlines():
        if "IEEE 802.11" in line:
            return line.split()[0]  # Extract the interface name
    return None

def scan_networks(interface):
    """
    Scan for nearby Wi-Fi networks and parse the results.
    """
    output = run_command(f"sudo airodump-ng {interface}mon")
    networks = []
    network_re = re.compile(r'([0-9A-F:]{17})\s+\d+\s+(\d+)\s+-\d+\s+-\d+\s+\d+\s+\S+\s+(.+)')

    for line in output.splitlines():
        match = network_re.search(line)
        if match:
            bssid, channel, essid = match.groups()
            networks.append((bssid, channel, essid.strip()))
    
    return networks

def display_network_list(stdscr, networks):
    """
    Display a list of detected networks and allow the user to select one.
    """
    selected = 0
    while True:
        stdscr.clear()
        stdscr.border(0)
        stdscr.addstr(1, 2, "Select a Network", curses.A_BOLD)
        
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
        elif key == ord('\n'):  # Enter key
            return networks[selected]
        elif key == 27:  # Escape key to cancel
            return None

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(0)
    
    # Check dependencies before starting
    dependencies_status = check_dependencies()
    if dependencies_status:
        stdscr.addstr(10, 2, dependencies_status)
        stdscr.getch()
        sys.exit(1)

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

    # Enable mouse and keyboard interaction
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    stdscr.keypad(True)

    selected_network = None

    while True:
        draw_menu(stdscr)
        choice = stdscr.getch()

        # Handle menu actions
        if choice == ord('1'):  # Scan for Networks
            enable_monitor_mode(interface)
            stdscr.addstr(10, 2, "Scanning for networks...")
            stdscr.refresh()

            networks = scan_networks(interface)
            disable_monitor_mode(interface)

            if networks:
                selected_network = display_network_list(stdscr, networks)
                if selected_network:
                    stdscr.addstr(12, 2, f"Selected Network: {selected_network[2]} (BSSID: {selected_network[0]})")
                else:
                    stdscr.addstr(12, 2, "No network selected.")
            else:
                stdscr.addstr(12, 2, "No networks found.")
            stdscr.getch()

        elif choice == ord('2'):  # Capture WPA Handshake
            if selected_network:
                stdscr.addstr(10, 2, f"Capturing handshake for {selected_network[2]} (BSSID: {selected_network[0]})")
                curses.echo()
                bssid = selected_network[0]
                channel = selected_network[1]
                enable_monitor_mode(interface)
                output = capture_handshake(bssid, channel, interface)
                disable_monitor_mode(interface)
                stdscr.addstr(15, 2, output)
            else:
                stdscr.addstr(10, 2, "No network selected. Please scan and select a network first.")
            stdscr.getch()

        elif choice == ord('3'):  # Crack WPA Password
            if selected_network:
                stdscr.addstr(10, 2, "Enter path to wordlist: ")
                wordlist = stdscr.getstr(11, 2, 50).decode()
                bssid = selected_network[0]
                output = crack_wpa_handshake(wordlist, bssid)
                stdscr.addstr(15, 2, output)
            else:
                stdscr.addstr(10, 2, "No network selected. Please scan and select a network first.")
            stdscr.getch()

        elif choice == ord('4'):  # WPS Attack
            if selected_network:
                stdscr.addstr(10, 2, f"Running WPS attack on {selected_network[2]} (BSSID: {selected_network[0]})")
                bssid = selected_network[0]
                enable_monitor_mode(interface)
                output = wps_attack(bssid, interface)
                disable_monitor_mode(interface)
                stdscr.addstr(15, 2, output)
            else:
                stdscr.addstr(10, 2, "No network selected. Please scan and select a network first.")
            stdscr.getch()

        elif choice == ord('5'):  # Port Scan
            stdscr.addstr(10, 2, "Enter IP of the router: ")
            ip = stdscr.getstr(11, 2, 20).decode()
            output = port_scan(ip)
            stdscr.addstr(13, 2, output)
            stdscr.getch()

        elif choice == ord('6'):  # Exit
            exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rasengan: Wi-Fi Security Checker")
    args = parser.parse_args()
    curses.wrapper(main)