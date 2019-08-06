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

    def imprimir(self):
        temp = self.head.next
        print(self.head.info)
        while temp is not self.head:
            print(temp.info)
            temp = temp.next
