import curses
import curses.textpad
import argparse
import sys
import re
import shutil
import subprocess
import logging
from tools import check_tools_installed, enable_monitor_mode, disable_monitor_mode, run_command, find_wireless_interface, scan_networks
from attacks import capture_handshake, crack_wpa_handshake, wps_attack, port_scan
from menu import draw_menu

logging.basicConfig(level=logging.INFO)

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

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    # Check for dependencies
    dependency_status = check_dependencies()
    if dependency_status:
        logging.error(dependency_status)
        sys.exit(1)
    else:
        logging.info("All dependencies are installed.")

    # Find wireless interface
    interface = find_wireless_interface()
    if not interface:
        logging.error("No wireless interface found. Exiting.")
        sys.exit(1)
    
    # Enable monitor mode
    monitor_interface = enable_monitor_mode(interface)

    try:
        # Draw the main menu
        draw_menu(stdscr)
        
        # Example of scanning networks after user input
        networks = scan_networks(monitor_interface)
        if "Command failed" in networks or "Operation cancelled" in networks:
            logging.error("Network scan failed or was cancelled.")
        else:
            logging.info("Networks detected:")
            logging.info(networks)
    finally:
        # Disable monitor mode on exit
        disable_monitor_mode(monitor_interface)

if __name__ == "__main__":
    curses.wrapper(main)