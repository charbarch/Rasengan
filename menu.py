import curses

def setup_colors():
    # Initialize color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Header
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Menu options
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Highlight active option
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Footer

def draw_menu(stdscr):
    setup_colors()
    stdscr.clear()
    stdscr.border(0)
    
    # Use color pair 1 for the header
    stdscr.addstr(1, 2, "Rasengan: Wi-Fi Security Checker", curses.A_BOLD | curses.color_pair(1))
    
    # Use color pair 2 for the options
    stdscr.addstr(3, 2, "[1] Scan for Networks", curses.color_pair(2))
    stdscr.addstr(4, 2, "[2] Capture WPA Handshake", curses.color_pair(2))
    stdscr.addstr(5, 2, "[3] Crack WPA Password", curses.color_pair(2))
    stdscr.addstr(6, 2, "[4] WPS Attack", curses.color_pair(2))
    stdscr.addstr(7, 2, "[5] Port Scan", curses.color_pair(2))
    stdscr.addstr(8, 2, "[6] Exit", curses.color_pair(2))
    
    # Use default colors for the prompt
    stdscr.addstr(10, 2, "Choose an option: ")
    
    # Use color pair 4 for the footer
    stdscr.addstr(28, 60, "Created by: Chararch | GitHub: https://github.com/charbarch", curses.A_DIM | curses.color_pair(4))

    stdscr.refresh()
    stdscr.getch()

# Run the program
curses.wrapper(draw_menu)