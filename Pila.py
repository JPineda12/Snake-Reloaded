class Nodo:
    def __init__(self,x,y,valor):
        self.x=x
        self.y=y
        self.valor=valor
        self.sig=None
    
class Pila:

    def __init__(self):
        self.inicio=None
        self.size=0
    
    def push(self,x,y,valor):
        if self.inicio is None:
            self.inicio=Nodo(x,y,valor)
            
        else:
            nuevo_Nodo=Nodo(x,y,valor)
            nuevo_Nodo.sig=self.inicio
            self.inicio.anterior=nuevo_Nodo
            self.inicio=nuevo_Nodo
        self.size+=1
    
    def pop(self):
        if self.inicio is None:
            self.inicio=None
        else:
            self.inicio=self.inicio.sig
    def peek(self):
        return self.inicio