class Nodo:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.sig=None
        self.anterior=None
class lista:
    def __init__(self):
        self.inicio=None
        self.size=0

    def insertar_inicio(self,x,y):
        if self.inicio is None:
            nuevo_Nodo=Nodo(x,y)
            self.inicio=nuevo_Nodo
            
        else:
            nuevo_Nodo=Nodo(x,y)
            nuevo_Nodo.sig=self.inicio
            self.inicio.anterior=nuevo_Nodo
            self.inicio=nuevo_Nodo
        self.size+=1
        
    def insertar_final(self,x,y):
        if self.inicio is None:
            nuevo_Nodo=Nodo(x,y)
            self.inicio=nuevo_Nodo
        else:
            temp=self.inicio
            while temp.sig is not None:
                temp=temp.sig
            nuevo_Nodo=Nodo(x,y)
            temp.sig=nuevo_Nodo
            nuevo_Nodo.anterior=temp
        self.size+=1

    def insertar_pos(self,index,x,y):
        if self.inicio is None:
            print("Lista Vacia")
        else:
            if index<0 or index>=self.size:
                pass
            else:
                if index==0:
                    self.insertar_inicio(x,y)
                elif index==self.size-1:
                    self.insertar_final(x,y)
                elif index>0 and index<self.size-1:
                    nuevo_Nodo=Nodo(x,y)
                    temp=self.inicio
                    count = 0
                    while count!=index:
                        count+=1
                        nodoanterior=temp
                        temp=temp.sig
                    nodoanterior.sig=nuevo_Nodo
                    nuevo_Nodo.sig=temp


            self.size+=1
                                
    def obtener_pos(self, index):
        if index<0 or index>=self.size:
            pass
        else:
            temp=self.inicio
            count=0
            while(count!=index):
                temp=temp.sig
                count+=1
            return temp

    def eliminar(self,index):
        if index<0 or index>self.size-1:
            pass
        else:
            temp=self.inicio
            count=0
            if index>0:
                while(count!=index):
                    previo=temp
                    temp=temp.sig
                    count+=1

                temp=temp.sig
                previo.sig=temp
            elif index==0:
                self.inicio=temp.sig

        self.size-=1

    def imprimir(self):
        temp=self.inicio
        while(temp!=None):
            print("("+str(temp.x)+","+str(temp.y)+")")
            temp=temp.sig
    def getSize(self):
        return self.size
        
    def graficar(self):
        file = open("grafica.dot","w") 
        file.write("digraph foo {\n")
        file.write("rankdir=LR;\n")
        file.write("node [shape=record];\n")
        temp=self.inicio
        for x in range(0,self.size):
            file.write(str(x)+" [label=\"{ <data> "+str(temp,x)+"| <ref>  }\", width=1.2]\n")
            temp=temp.sig           
        for y in range(0,self.size-1):
            file.write(str(y)+" -> "+str(y+1)+"\n")
            file.write(str(y+1)+" ->"+str(y)+"\n")
        file.write("}")
        file.close() 

        import os
        os.system("dot grafica.dot -Tpng -o graf.png")
        os.system("eog graf.png")




