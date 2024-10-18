
import curses

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
