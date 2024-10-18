import curses
import logging
from attacks import capture_handshake, crack_wpa_handshake, wps_attack, port_scan

logging.basicConfig(level=logging.INFO)

def setup_colors():
    # Initialize color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Header
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Menu options
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Highlight active option
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Footer

def draw_menu(stdscr):
    setup_colors()
    k = 0
    cursor_y = 0

    while k != ord('6'):
        # Get screen height and width
        height, width = stdscr.getmaxyx()

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.border(0)

        # Calculate centered positions
        title = "Rasengan: Wi-Fi Security Checker"
        title_x = (width // 2) - (len(title) // 2)
        menu_start_y = 3

        # Draw header
        stdscr.addstr(1, title_x, title, curses.A_BOLD | curses.color_pair(1))

        # Draw menu options
        menu_options = [
            "1 - Scan for available Wi-Fi networks",
            "2 - Capture WPA/WPA2 handshake",
            "3 - Crack WPA/WPA2 handshake",
            "4 - Perform WPS attack",
            "5 - Perform port scan",
            "6 - Exit"
        ]

        for idx, option in enumerate(menu_options):
            x = 2
            y = menu_start_y + idx * 2
            if cursor_y == idx:
                stdscr.addstr(y, x, option, curses.A_REVERSE | curses.color_pair(2))
            else:
                stdscr.addstr(y, x, option, curses.color_pair(2))

        # Refresh screen
        stdscr.refresh()

        # Wait for user input
        k = stdscr.getch()

        if k == curses.KEY_UP and cursor_y > 0:
            cursor_y -= 1
        elif k == curses.KEY_DOWN and cursor_y < len(menu_options) - 1:
            cursor_y += 1
        elif k == ord('\n'):
            if cursor_y == 1:
                # Capture WPA/WPA2 handshake
                bssid = "00:11:22:33:44:55"  # Example BSSID
                channel = "6"  # Example channel
                interface = "wlan0"  # Example interface
                capture_handshake(bssid, channel, interface)
            elif cursor_y == 2:
                # Crack WPA/WPA2 handshake
                wordlist = "wordlist.txt"  # Example wordlist path
                bssid = "00:11:22:33:44:55"  # Example BSSID
                crack_wpa_handshake(wordlist, bssid)
            elif cursor_y == 3:
                # Perform WPS attack
                bssid = "00:11:22:33:44:55"  # Example BSSID
                interface = "wlan0"  # Example interface
                wps_attack(bssid, interface)
            elif cursor_y == 4:
                # Perform port scan
                target_ip = "192.168.1.1"  # Example target IP
                port_scan(target_ip)
            elif cursor_y == 5:
                # Exit the program
                break

        # Exit the program if '6' is pressed
        if k == ord('6'):
            break

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()