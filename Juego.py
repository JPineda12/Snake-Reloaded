import curses
from curses import textpad
from listaDoble import lista
from Pila import Pila
import random

height=20
width=60
def checkWalls(pos_x,pos_y): #Function that check the collisions with the walls
        
    #Pared izquierda X=0 y=y
    if (pos_x) is 0:
        pos_x=width-2      
    #Pared Derecha x=width y=y
    elif (pos_x) is width-1:
        pos_x=1
    #Pared Superior x=x y=0
    elif (pos_y) is 0:
        pos_y=height-2
    #Pared inferior x=x y=height
    elif (pos_y) is height-1:    
        pos_y=1
    return pos_x,pos_y

def checkGameOver(pos_x,pos_y,snake): #Function to check if the snake is gonna touch itself
    for i in range(0,snake.getSize()):
        if  pos_x is snake.obtener_pos(i).x and pos_y is snake.obtener_pos(i).y:
            return True

    return False

def createFood(snake):
    foodx=None                            #x coord for the food
    foody=None                            #y coord for the food
    tipo=None                             # + or * food
    while foodx is None:
        foodx=random.randint(1,width-3) #x coord between the walls
        for i in range(0,snake.getSize()-1):
            if foodx==snake.obtener_pos(i).x:
                foodx=None
    while foody is None:
        foody=random.randint(1,height-2)
        for i in range(0,snake.getSize()-1):
            if foody==snake.obtener_pos(i).y:
                foody=None
    #print("("+str(foodx)+","+str(foody))
    tipo=random.choice(['*','+'])
    if snake.getSize is 3:
        tipo='+'
    return foodx,foody,tipo #Returning the x and y coordenates to created the food



def jugar(user):
    import curses #import the curses library
    from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN #import special KEYS from the curses library

    stdscr = curses.initscr() #initialize console
    height = 20
    width = 60
    pos_y = 0
    pos_x = 0
    window = curses.newwin(height,width,pos_y,pos_x) #create a new curses window
    window.keypad(True)     #enable Keypad mode
    curses.noecho()         #prevent input from displaying in the screen
    curses.curs_set(0)      #cursor invisible (0)
    window.border(0)        #default border for our window
    window.nodelay(True)    #return -1 when no key is pressed

    score=0 #Score Variable starts at 0
    usuario=user #User Var
    #Adding text strings to the top of the windows
    textosc='Score: '+str(score)
    textosn='SNAKE RELOADED:'
    textous='User: '+usuario
    window.addstr(0,5,textosc)
    window.addstr(0,(width/2)-10,textosn)
    window.addstr(0,(width-len(textous))-2,textous)

    scorePila=Pila()

    key = KEY_RIGHT         #key defaulted to KEY_RIGHT
    pos_x = 4               #initial x position
    pos_y = 4               #initial y position
    
    #Creating the Snake
    snake=lista()#Setting up the doubly linked list for the snake
    #inserting the initial positions of the snake
    snake.insertar_inicio(pos_x,pos_y) 
    snake.insertar_inicio((pos_x-1),(pos_y))
    snake.insertar_inicio((pos_x-2),(pos_y))
    
    food_x,food_y,tipo=createFood(snake)
    scorePila.push(food_x,food_y,tipo)
    window.addch(food_y,food_x,tipo)
    time=500
    gameOver=False
    #window.addch(pos_y,pos_x,'*')   #print initial dot
    while key != 27:                #run program while [ESC] key is not pressed
        if gameOver is False:
            window.timeout(time)         #delay of 100 milliseconds
            keystroke = window.getch()  #get current key being pressed
            

            if keystroke is not  -1:    #key is pressed
                key = keystroke         #key direction changes
            
            

            if key == KEY_RIGHT:                #right direction
                pos_x,pos_y=checkWalls(pos_x+1,pos_y)        #Check if can increase posy
            elif key == KEY_LEFT:               #left direction
                pos_x,pos_y=checkWalls(pos_x-1,pos_y)        #Check if can decrease posy
            elif key == KEY_UP:                 #up direction
                pos_x,pos_y=checkWalls(pos_x,pos_y-1)        #Check if can decrease posy
            elif key == KEY_DOWN:               #down direction
                pos_x,pos_y=checkWalls(pos_x,pos_y+1)        #Check if can decrease posy
                
            gameOver=checkGameOver(pos_x,pos_y,snake) #Snake has touched the wall 

            if gameOver:
                window.addstr(10,20,"Game Over!") 
            else:
                snake.insertar_inicio(pos_x,pos_y)
                
                if snake.obtener_pos(0).x is food_x and snake.obtener_pos(0).y is food_y:
                    food_x,food_y,tipo=createFood(snake) #Creates a new food in random pos
                    if scorePila.peek().valor is '+':   
                        score+=2
                        scorePila.push(food_x,food_y,tipo) # Pushes the new food in the stack
                    elif scorePila.peek().valor is '*':
                        score-=2
                        scorePila.pop()                     # Pops the bad food from the stack
                        snakelast=snake.getSize()-1
                        window.addch(snake.obtener_pos(snakelast).y,snake.obtener_pos(snakelast).x,' ')#Erase the last dot
                        snake.eliminar(snakelast)
                    
                    window.addch(food_y,food_x,tipo)      
                    textosc='Score: '+str(score)
                    window.addstr(0,5,textosc)
                else: 
                    snakelast=snake.getSize()-1
                    window.addch(snake.obtener_pos(snakelast).y,snake.obtener_pos(snakelast).x,' ')#Erase the last dot
                    snake.eliminar(snakelast)
                for i in range(0,snake.getSize()):
                    window.addch(snake.obtener_pos(i).y,snake.obtener_pos(i).x,'#')
            window.refresh() 
        #window.addstr(0,0,'Size: '+str(snake.getSize()))
        
        else: 
            back=window.getch()
            if back is not -1:
                break
    #if key is not -1:
        #curses.endwin() #return terminal to previous state

    