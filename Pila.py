class Nodo:
    def __init__(self, x, y, valor):
        self.x = x
        self.y = y
        self.valor = valor
        self.sig = None


# Stack for that holds the coords of the food
class Pila:

    def __init__(self):
        self.inicio = None
        self.size = 0

    def push(self, x, y, valor):
        if self.inicio is None:
            self.inicio = Nodo(x, y, valor)

        else:
            nuevo_Nodo = Nodo(x, y, valor)
            nuevo_Nodo.sig = self.inicio
            self.inicio.anterior = nuevo_Nodo
            self.inicio = nuevo_Nodo
        self.size += 1

    def pop(self):
        if self.inicio is None:
            self.inicio = None
        else:
            self.inicio = self.inicio.sig
        self.size -= 1

    def peek(self):
        return self.inicio

    def printpop(self):
        while self.size is not 0:
            print(""+str(self.inicio.x)+","+str(self.inicio.y)+","+str(self.inicio.valor))  # noqa
            self.pop()

    def graficar(self):
        file = open("graficaStack.dot", "w")
        file.write("digraph foo {\n")
        file.write("rankdir=LR;\n")
        file.write("node [shape=record];\n")
        temp = self.inicio
        for x in range(0, self.size):
            # a [label="{ <data> (breSt12,15) | <ref>  }", width=1.9]
            file.write(str(x)+" [label=\"{ <data> ("+str(temp.valor)+"| <ref>  }\", width=1.2]\n")  # noqa
            temp = temp.sig
        for y in range(0, self.size-1):
            file.write(str(y)+" -> "+str(y+1)+"\n")
            file.write(str(y+1)+" ->"+str(y)+"\n")
        file.write("}")
        file.close()

        import os
        os.system("dot graficaStack.dot -Tpng -o Stack.png")
        os.system("eog Stack.png")

    def getSize(self):
        return self.size
