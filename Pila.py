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
        if self.size > 0:
            file = open("stack.dot", "w")
            file.write("digraph foo {\n")
            file.write("node [shape=record];\n")
            temp = self.inicio.sig
            file.write("pila [label=\"{")
            while temp is not None:
                if temp.valor is '+':
                    file.write("|("+str(temp.x)+","+str(temp.y)+")")  # noqa
                temp = temp.sig
            file.write("}\"];\n")
            file.write("}")
            file.close()
            import os
            os.system("dot stack.dot -Tpng -o stack.png")
            os.system("eog stack.png")
            return True

        return False

    def getSize(self):
        return self.size
