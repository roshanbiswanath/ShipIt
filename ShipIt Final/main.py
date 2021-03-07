import curses
import os, subprocess, sys

menu = [ 'Admin', 'Customer', 'Exit']

currentpath =  os.path.dirname(sys.argv[0])

def drawborder(screen):
    y,x = screen.getmaxyx()
    screen.addstr(0,0,"░")
    screen.addstr(0,x-1,"░")
    screen.addstr(y-2,0,"░")
    screen.addstr(y-2,x-1,"░")
    for i in range(1,x-2):
        screen.addstr(0,i,"░░")
        screen.addstr(y-2,i,"░░")
    for i in range(1,y-2):
        screen.addstr(i,0,"░░")
        screen.addstr(i,x-2,"░░")
    screen.refresh()

def print_menu(stdscr, selected_row_idx):
    l = [
        "░██████╗██╗░░██╗██╗██████╗░██╗████████╗",
        "██╔════╝██║░░██║██║██╔══██╗██║╚══██╔══╝",
        "╚█████╗░███████║██║██████╔╝██║░░░██║░░░",
        "░╚═══██╗██╔══██║██║██╔═══╝░██║░░░██║░░░",
        "██████╔╝██║░░██║██║██║░░░░░██║░░░██║░░░",
        "╚═════╝░╚═╝░░╚═╝╚═╝╚═╝░░░░░╚═╝░░░╚═╝░░░"]
    h, w = stdscr.getmaxyx()
    w = w//2
    stdscr.clear()
    
    for i in range(0,len(l)):
        x = w + w//2 - len(l[i])//2
        y = h//2 - len(l)//2 + i
        stdscr.addstr(y, x, l[i])

    drawborder(stdscr)
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def print_center(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2 - len(text)//2
    y = h//2
    stdscr.addstr(y, x, text)
    stdscr.refresh()

def start(stdscr) :
    global current_row
    stdscr.bkgd(' ', curses.color_pair(2) | curses.A_BOLD)
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
    stdscr = curses.initscr()
    curses.resize_term(20,130)
    current_row = 0
    stdscr.refresh()
    print_menu(stdscr, current_row)
    stdscr.refresh()
    while 1:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu)-1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == len(menu)-1:
                break
            else:
                break
        print_menu(stdscr, current_row)
curses.wrapper(start)
if current_row == 1:
    subprocess.call(["python.exe",  currentpath + "/ShipIt_User_col.py"])
elif current_row == 0:
    subprocess.call(["python.exe",  currentpath + "/ShipIt_Admin_col.py"])

