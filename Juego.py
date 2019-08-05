import curses
from curses import textpad
from listaDoble import lista

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

    score=5 #Score Variable starts at 0
    usuario=user #User Var
    #Adding text strings to the top of the windows
    textosc='Score: '+str(score)
    textosn='SNAKE RELOADED:'
    textous='User: '+usuario
    window.addstr(0,5,textosc)
    window.addstr(0,(width/2)-10,textosn)
    window.addstr(0,(width-len(textous))-2,textous)

    

    key = KEY_RIGHT         #key defaulted to KEY_RIGHT
    pos_x = 4               #initial x position
    pos_y = 4               #initial y position
    
    #Creating the Snake
    snake=lista()#Setting up the doubly linked list for the snake
    #inserting the initial positions of the snake
    snake.insertar_inicio(pos_x,pos_y) 
    snake.insertar_inicio((pos_x-1),(pos_y))
    snake.insertar_inicio((pos_x-2),(pos_y))
    
    
    #window.addch(pos_y,pos_x,'*')   #print initial dot
    while key != 27:                #run program while [ESC] key is not pressed
        window.timeout(1400)         #delay of 100 milliseconds
        keystroke = window.getch()  #get current key being pressed
         

        if keystroke is not  -1:    #key is pressed
            key = keystroke         #key direction changes
        
        

        if key == KEY_RIGHT:                #right direction
            pos_x = pos_x + 1               #pos_x increase

            pos_x,pos_y=checkWalls(pos_x,pos_y)        #Check the limits

            
        elif key == KEY_LEFT:               #left direction
            pos_x = pos_x - 1               #pos_x decrease
            pos_x,pos_y=checkWalls(pos_x,pos_y)        #Check the limits
        elif key == KEY_UP:                 #up direction
            pos_y = pos_y - 1               #pos_y decrease
            pos_x,pos_y=checkWalls(pos_x,pos_y)        #Check the limits
        elif key == KEY_DOWN:               #down direction
            pos_y = pos_y + 1               #pos_y increase
            pos_x,pos_y=checkWalls(pos_x,pos_y)        #Check the limits
        #window.addch(pos_y,pos_x,'*')       #draw new dot
        snake.insertar_inicio(pos_x,pos_y)
        
        
        snakelast=snake.getSize()-1
        window.addch(snake.obtener_pos(snakelast).y,snake.obtener_pos(snakelast).x,' ')#Erase the last dot
        snake.eliminar(snakelast)

        for i in range(0,snake.getSize()):
            window.addch(snake.obtener_pos(i).y,snake.obtener_pos(i).x,'#') 
        #window.addstr(0,0,'Size: '+str(snake.getSize()))
    curses.endwin() #return terminal to previous state

    