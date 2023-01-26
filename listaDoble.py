class Nodo:
    def __init__(self, x, y, key):
        self.x = x
        self.y = y
        self.key = key
        self.sig = None
        self.anterior = None


# List for the snake
class lista:
    def __init__(self):
        self.inicio = None
        self.size = 0

    def insertar_inicio(self, x, y, key):
        if self.inicio is None:
            nuevo_Nodo = Nodo(x, y, key)
            self.inicio = nuevo_Nodo
        else:
            nuevo_Nodo = Nodo(x, y, key)
            nuevo_Nodo.sig = self.inicio
            self.inicio.anterior = nuevo_Nodo
            self.inicio = nuevo_Nodo
        self.size += 1

    def insertar_final(self, x, y, key):
        if self.inicio is None:
            nuevo_Nodo = Nodo(x, y, key)
            self.inicio = nuevo_Nodo
        else:
            temp = self.inicio
            while temp.sig is not None:
                temp = temp.sig
            nuevo_Nodo = Nodo(x, y, key)
            temp.sig = nuevo_Nodo
            nuevo_Nodo.anterior = temp
        self.size += 1

    def insertar_pos(self, index, x, y, key):
        if self.inicio is None:
            print("Lista Vacia")
        else:
            if index < 0 or index >= self.size:
                pass
            else:
                if index == 0:
                    self.insertar_inicio(x, y, key)
                elif index == self.size-1:
                    self.insertar_final(x, y, key)
                elif index > 0 and index < self.size-1:
                    nuevo_Nodo = Nodo(x, y, key)
                    temp = self.inicio
                    count = 0
                    while count != index:
                        count += 1
                        nodoanterior = temp
                        temp = temp.sig
                    nodoanterior.sig = nuevo_Nodo
                    nuevo_Nodo.sig = temp

            self.size += 1

    def obtener_pos(self, index):
        if index < 0 or index >= self.size:
            pass
        else:
            temp = self.inicio
            count = 0
            while (count != index):
                temp = temp.sig
                count += 1
            return temp

    def reverse_headtail(self):  # function that reverses the list
        temp = None
        cur = self.inicio
        while cur is not None:
            temp = cur.anterior
            cur.anterior = cur.sig
            cur.sig = temp
            cur = cur.anterior
        if temp is not None:
            self.inicio = temp.anterior

    def eliminar(self, index):
        if index < 0 or index > self.size-1:
            pass
        else:
            temp = self.inicio
            count = 0
            if index > 0:
                while (count != index):
                    previo = temp
                    temp = temp.sig
                    count += 1

                temp = temp.sig
                previo.sig = temp
            elif index == 0:
                self.inicio = temp.sig

        self.size -= 1

    def imprimir(self):
        temp = self.inicio
        while (temp is not None):
            print("("+str(temp.x)+","+str(temp.y)+")")
            temp = temp.sig

    def getSize(self):
        return self.size

    def graficar(self):
        if self.size > 0:
            file = open("Reportes/graficaDoble.dot", "w")
            file.write("digraph foo {\n")
            file.write("rankdir=LR;\n")
            file.write("node [shape=record];\n")
            temp = self.inicio
            file.write("pf [label=\"{ <data> null}\", width=1.2]\n")
            for x in range(0, self.size):
                file.write("p"+str(x)+" [label=\"{ <data> ("+str(temp.x)+","+str(temp.y)+")"+"| <ref>  }\", width=1.2]\n")  # noqa
                temp = temp.sig
            file.write("pl [label=\"{ <data> null}\", width=1.2]\n")
            n = 0
            for y in range(0, self.size-1):
                file.write("p"+str(y)+" -> p"+str(y+1)+"\n")
                file.write("p"+str(y+1)+" ->p"+str(y)+"\n")
                n += 1
            file.write("p0-> pf\n")
            file.write("pf-> p0:data[arrowhead=none]\n")
            file.write("p"+str(n)+" -> pl\n")
            file.write("}")
            file.close()
            from sys import platform
            import os
            os.system("dot Reportes/graficaDoble.dot -Tpng -o Reportes/grafsnake.png")
            if platform == "linux" or platform == "linux2":
                # linux
                os.system("eog Reportes/grafsnake.png")
            elif platform == "darwin":
                # OS X
                pass
            elif platform == "win32":
                # Windows...
                os.system("start Reportes/grafsnake.png")                
        
            return True
        return False
