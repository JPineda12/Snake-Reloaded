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

    def imprimir(self):
        temp = self.head
        while temp.next is not None:
            print(temp.info)
            temp = temp.next
