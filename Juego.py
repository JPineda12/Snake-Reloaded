import curses
from curses import textpad
from listaDoble import lista
from Pila import Pila
import random
height = 17
width = 45


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
        tipo = random.choice(['*', '+', '+', '+'])
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


def jugar(user):
    # import special KEYS from the curses library
    from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
    scorePila = Pila()
    # stdscr = curses.initscr() #initialize console
    pos_y = 0
    pos_x = 0
    window = curses.newwin(height, width, pos_y, pos_x)  # create a new window
    window.keypad(True)     # enable Keypad mode
    curses.noecho()         # prevent input from displaying in the screen
    curses.curs_set(0)      # cursor invisible (0)
    window.border(0)        # default border for our window
    window.nodelay(True)    # return -1 when no key is pressed
    score = 0               # Score Variable starts at 0
    usuario = user          # User Var
    # Adding text strings to the top of the windows
    lvl = 0
    # textlvl = 'Level:'+str(lvl)
    textosc = 'Score:'+str(score)
    textosn = 'SNAKE RELOADED'
    textous = 'User:'+usuario
    window.addstr(0, 2, textosc)
    # window.addstr(0, 1, textlvl)
    window.addstr(0, (width/2)-len(textosn)/2, textosn)
    window.addstr(0, (width-len(textous))-1, textous)
    key = KEY_RIGHT         # key defaulted to KEY_RIGHT
    pos_x = 4               # initial x position
    pos_y = 4               # initial y position

    # Creating the Snake
    # inserting the initial positions of the snake
    snake = lista()
    score = 0
    snake.insertar_inicio(pos_x, pos_y)
    snake.insertar_inicio((pos_x-1), (pos_y))
    snake.insertar_inicio((pos_x-2), (pos_y))
    for i in range(0, snake.getSize()):
        window.addch(snake.obtener_pos(i).y, snake.obtener_pos(i).x, '$')
    # Creating food
    food_x, food_y, tipo = createFood(snake, score, scorePila)
    window.addch(food_y, food_x, tipo)
    time = 300
    gameOver = False
    scoreFinal = 0
    while key != 27:              # run program while [ESC] key is not pressed
        if gameOver is False:
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
                lvl = lvl+1
                window.addstr(0, 2, textosc)

            if keystroke is not -1:     # key is pressed
                key = keystroke         # key direction changes

            if key == KEY_RIGHT:                # right direction
                pos_x, pos_y = checkWalls(pos_x+1, pos_y)
            elif key == KEY_LEFT:               # left direction
                pos_x, pos_y = checkWalls(pos_x-1, pos_y)
            elif key == KEY_UP:                 # up direction
                pos_x, pos_y = checkWalls(pos_x, pos_y-1)
            elif key == KEY_DOWN:               # down direction
                pos_x, pos_y = checkWalls(pos_x, pos_y+1)

            gameOver = checkGameOver(pos_x, pos_y, snake)
            if gameOver:
                window.addstr(10, 20, "Game Over!")
            else:
                snake.insertar_inicio(pos_x, pos_y)
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
                window.refresh()
        else:
            back = window.getch()
            if back is not -1:
                break
    return usuario, scoreFinal
