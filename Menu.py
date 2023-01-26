import time
import curses
import Juego as jg
from listaCircular import listaCircular
from Cola import Cola
from User import User
from listaDoble import lista
from Pila import Pila
menu = ['Play', 'Scoreboard', 'User Selection', 'Reports', 'Bulk loading', 'Exit']  # noqa
usuarios = listaCircular()
scores = Cola()
scorePila = Pila()
snake = lista()


# function to print the menu
def print_menu(stdscr, fila_actual, paused):
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    word = "Game Menu"
    if paused:
        word = "Game Paused"
    x = int(w//2 - len(word)//2)
    y = int(h/2 - len(menu)//2 - 1)
    stdscr.addstr(y, x, word)
    word = "-----------"
    x = w//2 - len(word)//2
    stdscr.addstr(y+1, x, word)

    for idx, row in enumerate(menu):
        x = int(w//2 - len(row)//2)
        y = int(h/2 - len(menu)//2 + idx + 1)
        if(idx == fila_actual):
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    x = w//2 - len(word)//2
    stdscr.addstr(y+1, x, word)
    stdscr.refresh()


def scoreBoard(stdscr):
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    stdscr = curses.newwin(20, 40, int(h/2-10), int(w/2-15))
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
        scores.unqueue()
    while temporal.get_Size() != 0:
        nombre = temporal.peek().info.getNombre()
        punteo = temporal.peek().info.getPunteo()
        scores.insert(User(nombre, punteo))
        temporal.unqueue()
    stdscr.refresh()
    back = stdscr.getch()
    if back != -1:
        return


def userSelection(stdscr, usuarios):
    from curses import KEY_RIGHT, KEY_LEFT, KEY_ENTER
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    stdscr = curses.newwin(20, 40, int(h/2-10), int(w/2-15))
    stdscr.keypad(True)     # enable Keypad mode
    curses.noecho()         # prevent input from displaying in the screen
    curses.curs_set(0)      # cursor invisible (0)
    stdscr.border(0)        # default border for our window
    stdscr.nodelay(True)    # return -1 when no key is pressed
    stdscr.border(0)
    stdscr.addstr(0, 20-2, "USERS")
    user = usuarios.get_pos(0)
    stdscr.addstr(7, 13, "<-")
    stdscr.addstr(7, 27, "->")
    stdscr.addstr(7, int(20-len(user.info.getNombre())/2), user.info.getNombre())
    stdscr.refresh()
    key = -1
    while key != 27:
        key = stdscr.getch()
        if key == KEY_RIGHT:                # right direction
            user = user.next
        elif key == KEY_LEFT:               # left direction
            user = user.prev
        elif key == KEY_ENTER or key in [10, 13]:
            break
        elif key == 27:
            return None
        stdscr.addstr(7, 20-5, "         ")  # Wipes out the space for the new name # noqa
        stdscr.addstr(7, int(20-len(user.info.getNombre())/2), user.info.getNombre())  # noqa
        stdscr.refresh()
    if user is None:
        return None
    return user.info


def snakeReports(stdscr, paused, gameOver, snake, scorePila, usuarios):
    fila = 0
    rMenu = ['Snake Report', 'Score Report', 'Scoreboard Report', 'Users Report', 'Back']  # noqa
    print_repMenu(stdscr, rMenu, fila)
    h, w = stdscr.getmaxyx()
    while 1:  # highlights the option according to the key pressed.
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and fila > 0:
            fila -= 1
        elif key == curses.KEY_DOWN and fila < len(rMenu)-1:
            fila += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if fila == len(rMenu)-1:
                break
            elif fila == 0:
                words = "Generating Snake Report...."
                words2 = " "
                stdscr.addstr(int(h/2), int(w/2-len(words)/2), words)
                stdscr.refresh()
                time.sleep(1.0)
                success = snake.graficar()
                if gameOver or paused:
                    if success:
                        stdscr.clear()
                        words = "Snake Report Generated!"
                    else:
                        words = "There is no snake to report"
                        words2 = "You have to play a game first."
                elif gameOver is False and paused is False:
                    stdscr.clear()
                    words = "There is no snake to report"
                    words2 = "You have to play a game first."
                stdscr.addstr(int(h/2), int(w/2-len(words)/2), words)
                stdscr.addstr(int((h/2)+1), int(w/2-len(words)/2), words2)
                stdscr.refresh()
                stdscr.getch()
            elif fila == 1:
                words = "Generating Score Report...."
                words2 = " "
                stdscr.addstr(int(h/2), int(w/2-len(words)/2), words)
                stdscr.refresh()
                time.sleep(1.0)
                success = scorePila.graficar()
                if gameOver or paused:
                    if success:
                        stdscr.clear()
                        words = "Score Report Generated!"
                elif gameOver is False and paused is False:
                    stdscr.clear()
                    words = "There is no score to report"
                    words2 = "You have to play a game first!"
                stdscr.addstr(int(h/2), int(w/2-len(words)/2), words)
                stdscr.addstr(int((h/2)+1), int(w/2-len(words)/2), words2)
                stdscr.refresh()
                stdscr.getch()
            elif fila == 2:
                words = "Generating Scoreboard Report...."
                stdscr.addstr(int(h/2), int(w/2-len(words)/2), words)
                stdscr.refresh()
                time.sleep(1.0)
                success = scores.graficar()
                if success:
                    stdscr.clear()
                    words = "Scoreboard Report Generated!"
                elif success is False:
                    stdscr.clear()
                    words = "There is no scoreboard to report!"
                stdscr.addstr(int(h/2), int(w/2-len(words)/2), words)
                stdscr.refresh()
                stdscr.getch()
            elif fila == 3:
                words = "Generating Users Report...."
                stdscr.addstr(int(h/2), int(w/2-len(words)/2), words)
                stdscr.refresh()
                time.sleep(1.0)
                success = usuarios.graficar()
                if success:
                    stdscr.clear()
                    words = "User Report Generated!"
                elif success is False:
                    stdscr.clear()
                    words = "There are no users to report!"
                stdscr.addstr(int(h/2), int(w/2-len(words)/2), words)
                stdscr.refresh()
                stdscr.getch()
        print_repMenu(stdscr, rMenu, fila)
        stdscr.refresh()
    return


def print_repMenu(stdscr, rMenu, fila_actual):
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    word = "Snake Reloaded Reports"
    # if paused:
    #    word = "Game Paused"
    x = int(w//2 - len(word)//2)
    y = int(h/2 - len(rMenu)//2 - 1)
    stdscr.addstr(y, x, word)
    word = "--------------------------"
    x = int(w//2 - len(word)//2)
    stdscr.addstr(y+1, x, word)

    for idx, row in enumerate(rMenu):
        x = int(w//2 - len(row)//2)
        y = int(h/2 - len(rMenu)//2 + idx + 1)
        if(idx == fila_actual):
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    x = w//2 - len(word)//2
    stdscr.addstr(y+1, x, word)
    stdscr.refresh()


# Function that asks for a Username to play
def CrearUser(stdscr, usuarios):
    curses.echo()
    stdscr.addstr(0, 0, "Usuario: ")
    usuarioActual = str(stdscr.getstr(0, 9, 7))
    curses.noecho()
    newUser = User(usuarioActual,0)
    usuarios.insert_last(newUser)
    stdscr.clear()
    return newUser


def readcsv(archivo, usuarios):
    if ".csv" in archivo.decode():
        n = len(archivo)
        archivo = archivo[:n-4]
    import csv
    try:
        with open(archivo.decode()+'.csv') as csvFile:
            reader = csv.reader(csvFile)
            line = 0
            for row in reader:
                if line == 0:
                    pass
                else:
                    usuarios.insert_last(User(""+str(row[0]), str(row[1])))
                    if scores.get_Size() == 10:
                        scores.unqueue()
                    scores.insert(User(""+str(row[0]), str(row[1])))
                line += 1
            return True
    except IOError:
        return False


def bulkloading(stdscr, usuarios):
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    word = "File's Name: "
    curses.echo()
    stdscr.addstr(int(h/2), int(w/2 - len(word) - 5), word)
    stdscr.refresh()
    archivo = stdscr.getstr(int(h/2), int(w/2 - len(word)/2)+2, 20)
    curses.noecho()
    if readcsv(archivo, usuarios):

        word = "All users Loaded!"
    else:
        word = "Wrong file name"
    stdscr.clear()
    stdscr.addstr(int(h/2), int(w/2 - len(word)/2), word)
    stdscr.refresh()

    return


# Function to go through the menu
def main(stdscr):
    curses.curs_set(0)
    selectedUser = None
    paused = False
    gameOver = False
    snake = lista()
    scorePila = Pila()
    usuarios = listaCircular()
    initialScore = 0
    finalScore = 0
    # Highlights the first option
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    fila = 0
    print_menu(stdscr, fila, paused)
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
                if selectedUser is None:
                    # If you haven't select a username, create a new one
                    selectedUser = CrearUser(stdscr, usuarios)

                # Starts a new game with the user selected
                # and returns the player and his score when the game ends
                player, initialScore, finalScore, paused, snake, scorePila, gameOver = jg.jugar(selectedUser, initialScore, finalScore, paused)  # noqa
                if paused:
                    selectedUser = player
                else:
                    selectedUser = None
                    initialScore = 0
                    # inserts the score of the player in the scores list
                    if scores.get_Size() == 10:
                        scores.unqueue()
                    scores.insert(User(player.getNombre(), finalScore))
                    finalScore = 0

            elif fila == 1:
                scoreBoard(stdscr)
                stdscr.refresh()
            elif fila == 2:
                if paused is False:
                        if usuarios.getSize():
                            selectedUser = userSelection(stdscr, usuarios)
                        else:
                            h, w = stdscr.getmaxyx()
                            words = "There's no usernames"
                            stdscr.addstr(int(h/2), int(w/2-len(words)/2), words)
                            stdscr.getch()
                            stdscr.refresh()
                else:
                    h, w = stdscr.getmaxyx()
                    words = "Can't select user when game's paused"
                    stdscr.addstr(h/2, w/2-len(words)/2, words)
                    stdscr.getch()
                stdscr.refresh()
            elif fila == 3:
                snakeReports(stdscr, paused, gameOver, snake, scorePila, usuarios)  # noqa
                stdscr.refresh()
            elif fila == 4:
                bulkloading(stdscr, usuarios)
                stdscr.refresh()
                stdscr.getch()

        print_menu(stdscr, fila, paused)

        stdscr.refresh()
curses.wrapper(main)
