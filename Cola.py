class Nodo:
    def __init__(self, info):
        self.info = info
        self.next = None


class Cola:
    def __init__(self):
        self.head = None
        self.size = 0

    def insert(self, info):
        if self.head is None:
            self.head = Nodo(info)
        else:
            temp = self.head
            while temp.next is not None:
                temp = temp.next
            temp.next = Nodo(info)
        self.size += 1

    def unqueued(self):
        if self.head is None:
            self.head = None
        else:
            self.head = self.head.next
        self.size -= 1

    def peek(self):
        return self.head

    def get_Size(self):
        return self.size

    def graficar(self):
        if self.size > 0:
            file = open("graficaCola.dot", "w")
            file.write("digraph foo {\n")
            file.write("rankdir=LR;\n")
            file.write("node [shape=record];\n")
            temp = self.head
            x = -1
            while temp is not None:
                x += 1
                file.write(str(x)+" [label=\"{ <data> ("+str(temp.info.getNombre())+","+str(temp.info.getPunteo())+") | <ref>  }\", width=1.9]\n")  # noqa
                temp = temp.next
            file.write("null [shape=box];\n")
            for y in range(0, self.size-1):
                file.write(str(y)+" -> "+str(y+1)+"\n")
            file.write(str(x)+" -> null\n")
            file.write("")
            file.write("}")
            file.close()

            import os
            os.system("dot graficaCola.dot -Tpng -o cola.png")
            os.system("eog cola.png")
            return True
        return False

    def imprimir(self):
        temp = self.head
        while temp.next is not None:
            print(temp.info)
            temp = temp.next
