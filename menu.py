import curses
import logging

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
    cursor_x = 0
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
            logging.info(f"Selected option {cursor_y + 1}")
            if cursor_y == 0:
                # Scan for available Wi-Fi networks
                stdscr.clear()
                stdscr.addstr(0, 0, "Scanning for available networks...")
                stdscr.refresh()
                logging.info("Initiating network scan...")
                # Placeholder for scanning functionality
            elif cursor_y == 1:
                # Capture WPA/WPA2 handshake
                logging.info("Capturing WPA/WPA2 handshake...")
            elif cursor_y == 2:
                # Crack WPA/WPA2 handshake
                logging.info("Cracking WPA/WPA2 handshake...")
            elif cursor_y == 3:
                # Perform WPS attack
                logging.info("Performing WPS attack...")
            elif cursor_y == 4:
                # Perform port scan
                logging.info("Performing port scan...")
            elif cursor_y == 5:
                # Exit the program
                break