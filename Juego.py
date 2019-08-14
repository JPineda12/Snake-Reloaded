import curses
from curses import textpad
from listaDoble import lista
from Pila import Pila
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN, KEY_ENTER
import random
height = 17
width = 45
lSnake = lista()
lScore = Pila()


def checkWalls(pos_x, pos_y):   # Function to check collisions with walls
    # Pared izquierda X=0 y=y
    if (pos_x) is 0:
        pos_x = width-2
    # Pared Derecha x=width y=y
    elif (pos_x) is width-1:
        pos_x = 1
    # Pared Superior x=x y=0
    elif (pos_y) is 0:
        pos_y = height-2
    # Pared inferior x=x y=height
    elif (pos_y) is height-1:
        pos_y = 1
    return pos_x, pos_y


def checkGameOver(pos_x, pos_y, snake):  # Snake is gonna touch itself
    for i in range(0, snake.getSize()):
        if pos_x is snake.obtener_pos(i).x and pos_y is snake.obtener_pos(i).y:
            return True
    return False


def createFood(snake, score, scorePila):
    foodx = None                            # x coord for the food
    foody = None                            # y coord for the food
    tipo = '+'                             # + or * food
    while foodx is None:
        foodx = random.randint(1, width-3)  # x coord between the walls
        for i in range(0, snake.getSize()-1):
            if foodx == snake.obtener_pos(i).x:
                foodx = None
    while foody is None:
        foody = random.randint(1, height-2)
        for i in range(0, snake.getSize()-1):
            if foody == snake.obtener_pos(i).y:
                foody = None
    # print("("+str(foodx)+","+str(foody))

    if score > 0 and score < 14:
        tipo = random.choice(['*', '+', '+', '+', '+'])
    scorePila.push(foodx, foody, tipo)
    return foodx, foody, tipo  # Returning the x,y coords to create the food


def createObstacle(snake, score, level, obstacles):
    obstacle_x = None
    obstacle_y = None
    tipo = random.choice(['h', 'v'])  # Horizontal or Vertical Obstacle
    # Generating the walls
    obstacle = None
    if tipo is 'h':
        if level is 1:
            obstacle = "--"
        elif level is 2:
            obstacle = "---"
        elif level > 2:
            obstacle = "-----"
    elif tipo is 'v':
        if level is 1:
            obstacle = "|"
        elif level is 2:
            obstacle = "|\n|"
        elif level > 3:
            obstacle = "|\n|\n|"
    # Generating the coords
    while obstacle_x is None:
        obstacle_x = random.randint(1, width-2)
        for i in range(0, snake.getSize()-1):
            if obstacle_x == snake.obtener_pos(i).x:
                obstacle_x = None
    while obstacle_y is None:
        obstacle_y = random.randint(1, height-2)
        for i in range(0, snake.getSize()-1):
            if obstacle_y == snake.obtener_pos(i).y:
                obstacle_y = None

    return obstacle, obstacle_x, obstacle_y


def jugar(user, punteo, scfinal, paused):

    stdscr = curses.initscr()  # initialize console
    pos_y = 0
    pos_x = 0
    h, w = stdscr.getmaxyx()
    window = curses.newwin(height, width, h/2-10, w/2-15)  # create new window
    window.keypad(True)     # enable Keypad mode
    curses.noecho()         # prevent input from displaying in the screen
    curses.curs_set(0)      # cursor invisible (0)
    window.border(0)        # default border for our window
    window.nodelay(True)    # return -1 when no key is pressed
    usuario = user          # User Var
    # Adding text strings to the top of the windows
    textosn = 'SNAKE RELOADED'
    textous = 'User:'+usuario
    window.addstr(0, (width/2)-len(textosn)/2, textosn)
    window.addstr(0, (width-len(textous))-1, textous)
    key = KEY_RIGHT
    pos_x = 4
    pos_y = 4
    # Creating the Snake
    # inserting the initial positions of the snake
    if paused is False:
        for n in range(0, lSnake.getSize()):
            lSnake.eliminar(n)
        for n in range(0, lScore.getSize()):
            lScore.pop()

    snake = lSnake
    scorePila = lScore
    if paused:
        score = punteo
    else:
        score = 0               # Score Variable starts at 0
    textosc = 'Score:'+str(score)
    window.addstr(0, 2, textosc)
    if snake.getSize() > 0:
        pos_x = snake.obtener_pos(0).x  # initial x position
        pos_y = snake.obtener_pos(0).y  # initial y position
        key = lSnake.obtener_pos(0).key
    if snake.getSize() is 0:
        snake.insertar_final(pos_x, pos_y, key)
        snake.insertar_final((pos_x-1), (pos_y), key)
        snake.insertar_final((pos_x-2), (pos_y), key)
    for i in range(0, snake.getSize()):
        window.addch(snake.obtener_pos(i).y, snake.obtener_pos(i).x, '$')
    # Creating food
    if paused:
        food_x = scorePila.peek().x
        food_y = scorePila.peek().y
        tipo = scorePila.peek().valor
    else:
        food_x, food_y, tipo = createFood(snake, score, scorePila)
    window.addch(food_y, food_x, tipo)
    time = 100
    gameOver = False
    paused = False
    scoreFinal = scfinal
    lastkey = -1
    while key != 27:              # run program while [ESC] key is not pressed
        if gameOver is False and paused is False:
            window.timeout(time)         # delay of 100 milliseconds
            keystroke = window.getch()  # get current key being pressed

            # Increase the game speed
            if score > 14:
                if time is 100:
                    time = time - 25
                elif time is 50:
                    time = 45
                elif time > 100:
                    time = time - 100
                score = 0
                textosc = 'Score:'+str(score)+" "
                window.addstr(0, 2, textosc)

            if keystroke in [KEY_DOWN, KEY_LEFT, KEY_UP, KEY_RIGHT, 80, 112, KEY_ENTER]:     # key is pressed # noqa
                key = keystroke         # key direction changes

            if key == KEY_RIGHT:                # right direction
                if lastkey == KEY_LEFT:
                    snake.reverse_headtail()
                    pos_x, pos_y = checkWalls(pos_x-1, pos_y)
                else:
                    pos_x, pos_y = checkWalls(pos_x+1, pos_y)
            elif key == KEY_LEFT:               # left direction
                if lastkey == KEY_RIGHT:
                    snake.reverse_headtail()
                    pos_x, pos_y = checkWalls(pos_x+1, pos_y)
                else:
                    pos_x, pos_y = checkWalls(pos_x-1, pos_y)
            elif key == KEY_UP:                 # up direction
                if lastkey == KEY_DOWN:
                    snake.reverse_headtail()
                    pos_x, pos_y = checkWalls(pos_x, pos_y+1)
                else:
                    pos_x, pos_y = checkWalls(pos_x, pos_y-1)
            elif key == KEY_DOWN:               # down direction
                if lastkey == KEY_UP:
                    snake.reverse_headtail()
                    pos_x, pos_y = checkWalls(pos_x, pos_y-1)
                else:
                    pos_x, pos_y = checkWalls(pos_x, pos_y+1)
            elif key in [80, 112, KEY_ENTER]:
                paused = True
            if paused is False:
                gameOver = checkGameOver(pos_x, pos_y, snake)
            if gameOver:
                window.addstr(10, 20, "Game Over!")
            elif paused:
                window.addstr(10, 20, "Paused!")
            else:
                snake.insertar_inicio(pos_x, pos_y, key)
                increase = False
                if pos_x is food_x and pos_y is food_y:
                    # Check if the food is good or bad
                    if scorePila.peek().valor is '+':
                        score = score + 2       # Adds to the score
                        scoreFinal = scoreFinal + 2
                        increase = True
                    elif scorePila.peek().valor is '*':
                        score = score - 2       # subtracts the score
                        scoreFinal = scoreFinal - 2
                        scorePila.pop()
                        scorePila.pop()
                        # Snake decreases
                        snakelast = snake.getSize()-1
                        window.addch(snake.obtener_pos(snakelast).y, snake.obtener_pos(snakelast).x, ' ')  # noqa Erase the last dot
                        snake.eliminar(snakelast)
                    textosc = 'Score:'+str(score)+" "
                    window.addstr(0, 2, textosc)
                    # create new food and display it
                    food_x, food_y, tipo = createFood(snake, score, scorePila)
                    window.addch(food_y, food_x, tipo)
                if increase is False:
                    snakelast = snake.getSize()-1
                    window.addch(snake.obtener_pos(snakelast).y, snake.obtener_pos(snakelast).x, ' ')  # noqa Erase the last dot
                    snake.eliminar(snakelast)
                for i in range(0, snake.getSize()):
                    window.addch(snake.obtener_pos(i).y, snake.obtener_pos(i).x, '$')  # noqa
                lastkey = key   # Saves the last key pressed to compare in the next iteration # noqa
                window.refresh()
        else:
            back = window.getch()
            if back is not -1:
                break
    return usuario, score, scoreFinal, paused, snake, lScore, gameOver
