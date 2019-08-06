
import time
import curses
import Juego as jg
from listaCircular import listaCircular
from Cola import Cola
from User import User
menu = ['Play', 'Scoreboard', 'User Selection', 'Reports', 'Bulk loading', 'Exit']  # noqa
usuarios = listaCircular()
scores = Cola()


# function to print the menu
def print_menu(stdscr, fila_actual):
    h, w = stdscr.getmaxyx()

    stdscr.clear()
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h/2 - len(menu)//2 + idx
        if(idx == fila_actual):
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()


def scoreBoard(stdscr):
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    stdscr = curses.newwin(20, 40, h/2-10, w/2-15)
    stdscr.border(0)
    stdscr.addstr(0, 20-5, "SCOREBOARD")

    stdscr.addstr(4, 12, "NAME")
    stdscr.addstr(4, 22, "SCORE")
    temporal = Cola()
    for i in range(0, scores.get_Size()):
        nombre = scores.peek().info.getNombre()
        punteo = scores.peek().info.getPunteo()
        stdscr.addstr(5+i, 12, nombre)
        stdscr.addstr(5+i, 23, str(punteo))
        temporal.insert(User(nombre, punteo))
        scores.unqueued()
    while temporal.get_Size() is not 0:
        nombre = temporal.peek().info.getNombre()
        punteo = temporal.peek().info.getPunteo()
        scores.insert(User(nombre, punteo))
        temporal.unqueued()
    stdscr.refresh()
    back = stdscr.getch()
    if back is not -1:
        return


# Function that asks for a Username to play
def CrearUser(stdscr):
    curses.echo()
    stdscr.addstr(0, 0, "Usuario: ")
    usuarioActual = stdscr.getstr(0, 9, 7)
    curses.noecho()
    usuarios.insert_last(User(""+usuarioActual, 0))
    return usuarioActual


# Function to go through the menu
def main(stdscr):
    curses.curs_set(0)
    # Highlights the first option
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    fila = 0
    print_menu(stdscr, fila)
    while 1:  # highlights the option according to the key pressed.
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and fila > 0:
            fila -= 1
        elif key == curses.KEY_DOWN and fila < len(menu)-1:
            fila += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if fila == len(menu)-1:
                stdscr.addstr(0, 0, "Saliendo del juego....")
                stdscr.refresh()
                time.sleep(1.5)
                break
            elif fila == 0:
                stdscr.clear()
                user = CrearUser(stdscr)
                # Starts a new game with the user selected
                # and returns the player and his score when the game ends
                player, finalScore = jg.jugar(user)
                # inserts the score of the player in the scores list
                if scores.get_Size() is 10:
                    scores.unqueued()
                scores.insert(User(player, finalScore))

            elif fila == 1:
                stdscr.addstr(0, 0, "ScoreBoard")
                scoreBoard(stdscr)
                stdscr.refresh()
                stdscr.getch()
            elif fila == 2:
                stdscr.addstr(0, 0, "User Selection")
                stdscr.refresh()
                stdscr.getch()
            elif fila == 3:
                stdscr.addstr(0, 0, "Reports")
                stdscr.refresh()
                stdscr.getch()
            elif fila == 4:
                stdscr.addstr(0, 0, "Bulk Loading")
                stdscr.refresh()
                stdscr.getch()

        print_menu(stdscr, fila)

        stdscr.refresh()
curses.wrapper(main)
