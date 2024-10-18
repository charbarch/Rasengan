import curses

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
            "[1] Scan for Networks",
            "[2] Capture WPA Handshake",
            "[3] Crack WPA Password",
            "[4] WPS Attack",
            "[5] Port Scan",
            "[6] Exit"
        ]

        for idx, option in enumerate(menu_options):
            x = 2
            y = menu_start_y + idx
            stdscr.addstr(y, x, option, curses.color_pair(2))

        # Draw footer
        footer_text = "Created by: Chararch | GitHub: charbarch (https://github.com/charbarch)"
        footer_x = (width // 2) - (len(footer_text) // 2)
        stdscr.addstr(height - 2, footer_x, footer_text, curses.A_DIM | curses.color_pair(4))

        # Refresh the screen
        stdscr.refresh()

        # Wait for user input
        k = stdscr.getch()

curses.wrapper(draw_menu)