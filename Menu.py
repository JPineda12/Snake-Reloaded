#Menu Principal de la Aplicacion
import time
import curses
import Juego as jg
menu = ['Play' , 'Scoreboard', 'User Selection','Reports','Bulk loading','Exit']

def print_menu(stdscr,fila_actual):
    h,w=stdscr.getmaxyx()

    stdscr.clear()
    for idx,row in enumerate(menu):
        x=w//2 - len(row)//2
        y=h/2 - len(menu)//2 +idx
        if(idx == fila_actual):
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y,x,row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y,x,row)

    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)
    fila=0
    print_menu(stdscr,fila)

    while 1:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and fila>0:
            fila-=1
        elif key == curses.KEY_DOWN and fila<len(menu)-1:
            fila+=1
        elif key == curses.KEY_ENTER or key in [10,13]: 
            if fila == len(menu)-1:
                stdscr.addstr(0,0,"Saliendo del juego....")
                stdscr.refresh()
                time.sleep(1.5)
                break
            elif fila == 0:
                stdscr.clear()
                jg.jugar()
            elif fila==1:
                stdscr.addstr(0,0,"ScoreBoard")
                stdscr.refresh()
                stdscr.getch()
            elif fila==2:
                stdscr.addstr(0,0,"User Selection")
                stdscr.refresh()
                stdscr.getch()
            elif fila==3:
                stdscr.addstr(0,0,"Reports")
                stdscr.refresh()
                stdscr.getch()
            elif fila==4:
                stdscr.addstr(0,0,"Bulk Loading")
                stdscr.refresh()
                stdscr.getch()
            
        print_menu(stdscr,fila)

        stdscr.refresh()

curses.wrapper(main)