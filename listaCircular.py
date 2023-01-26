class Nodo:
    def __init__(self, info):
        self.next = None
        self.prev = None
        self.info = info


class listaCircular:
    def __init__(self):
        self.head = None
        self.size = 0

    def insert_last(self, info):
        self.size += 1
        if self.head is None:
            nuevo = Nodo(info)
            nuevo.next = nuevo
            nuevo.prev = nuevo
            self.head = nuevo
        else:
            nuevo = Nodo(info)
            last = self.head.prev
            nuevo.next = self.head
            self.head.prev = nuevo
            nuevo.prev = last
            last.next = nuevo

    def insert_first(self, info):
        if self.head is None:
            nuevo = Nodo(info)
            nuevo.next = nuevo
            nuevo.prev = nuevo
            self.head = nuevo
        else:
            nuevo = Nodo(info)
            last = self.head.prev
            nuevo.next = self.head
            nuevo.prev = last
            last.next = nuevo
            self.head.prev = nuevo
            self.head = nuevo
        self.size += 1

    def get_pos(self, index):
        count = 0
        temp = self.head
        while count is not index:
            count += 1
            temp = temp.next
        return temp

    def getSize(self):
        return self.size

    def graficar(self):
        if self.size > 0:
            file = open("Reportes/graficaCircular.dot", "w")
            file.write("digraph foo {\n")
            file.write("rankdir=LR;\n")
            file.write("node [shape=record];\n")
            temp = self.head
            x = 0
            file.write("p"+str(x)+" [label=\"{<prev> | <data> "+str(temp.info.getNombre())+" | <next>}\", width=1.2]\n")  # noqa
            temp = temp.next
            while temp is not self.head:
                x += 1
                file.write("p"+str(x)+" [label=\"{<prev> | <data> "+str(temp.info.getNombre())+" | <next>}\", width=1.2]\n")  # noqa
                temp = temp.next
            file.write("{node[shape=point height=0] pf pl}\n")
            file.write("pf:n -> p0[arrowtail=none]\n")
            file.write("pf:s -> pl:s[dir=none]\n")
            for y in range(0, self.size-1):
                if y >= self.size-2:
                    file.write("p"+str(y)+":next:c -> p"+str(y+1)+";\n")
                    file.write("p"+str(y+1)+":prev:c -> p"+str(y)+";\n")
                else:
                    file.write("p"+str(y)+":next:c -> p"+str(y+1)+":prev;\n")
                    file.write("p"+str(y+1)+":prev:c -> p"+str(y)+":next;\n")
            file.write("p0:c -> p"+str(x)+":data\n")
            file.write("p"+str(x)+":next:c -> pl:n[arrowhead=none]\n")
            file.write("}")
            file.close()

            from sys import platform
            import os
            os.system("dot Reportes/graficaCircular.dot -Tpng -o Reportes/grafcirc.png")
            if platform == "linux" or platform == "linux2":
                # linux
                os.system("eog Reportes/grafcirc.png")
            elif platform == "darwin":
                # OS X
                pass
            elif platform == "win32":
                # Windows...
                os.system("start Reportes/grafcirc.png")

            return True

        return False

    def imprimir(self):
        temp = self.head.next
        print(self.head.info)
        while temp is not self.head:
            print(temp.info)
            temp = temp.next
