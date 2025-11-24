import os

#programa de colas de pedidos y almacenamiento de productos.

class HashItem:
    def __init__(self, key, value, cant):
        self.key = key
        self.value = value
        self.cant = cant
        
        
class HashTable:
    def __init__(self):
        self.size = 256
        self.slots = [None for i in range(self.size)]
        self.count = 0
        
        self._deleted = HashItem(None, None, None)
        
    def _hash(self, key):
        mult = 1
        hv = 0
        for ch in key:
            hv += mult * ord(ch)
            mult += 1
        return hv % self.size

    def put(self, key, value, cant):
        item = HashItem(key, value, cant)
        h = self._hash(key)
        while self.slots[h] is not None:
            if self.slots[h].key == key:
                break
            h = (h + 1) % self.size
        if self.slots[h] is None:
            self.count += 1
        self.slots[h] = item
        
    def put_interactivo(self):
        key = input("Ingrese la clave del producto: ")
        value = input("Ingrese el precio del producto: ")
        cant = input("ingrese la cantidad")
        self.put(key, value, cant)
        print("Producto agregado correctamente.\n")
    
    def get(self, key):
        h = self._hash(key) #computer hash for the given key
        while self.slots[h] is not None:
            if self.slots[h].key is key:
                return self.slots[h].value
            h = (h+ 1) % self.size
        return None
    def show_all(self):
        for slot in self.slots:
            if slot is not None and slot != self._deleted:
                print(f"{slot.key} : {slot.value}, cantidad: {slot.cant}")
                
    def delete(self, key):
        h = self._hash(key)

        while self.slots[h] is not None:
            if self.slots[h].key == key:
                self.slots[h] = self._deleted   # NO poner None
                self.count -= 1
                return True
        
            h = (h + 1) % self.size

        return False
    def delete_inter(self):
        key = input('ingresa la clave que deseas eliminar: ')
        self.delete(key)


class Node(object):
    def __init__(self, data=None, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev

class cola:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0
        
    def enqueue(self, data):
        new_node = Node(data, None, None)
        if self.head is None:
            self.head = new_node
            self.tail = self.head
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.count +=1
    def dequeue(self):
        current = self.head
        if self.count == 1:
            self.count -=1
            self.head = None
            self.tail = None
        elif self.count > 1:
            self.head = self.head.next
            self.head.prev = None
            self.count -=1 
        return current
    
class pedido:
    _contador_id = 1
    
    def __init__(self, solicitante, producto):
        self.id += 1
        self.solicitante = solicitante
        self.producto = producto
        



        
def inventario():
    inv.show_all()
    resp = int(input('que deseas hacer? \n 1. Insertar \n 2. Eliminar'))
    if resp == 1:
        inv.put_interactivo()
    elif resp == 2:
        inv.delete_inter()
    
    

inv = HashTable()

while True:
    
    os.system('cls')
    print("sistema de cola de pedidos e inventario")
    print('que desea hacer?')
    print('1. ver inventario:')
    print('2. ver cola')
    resp = int(input())
    
    if resp == 1:
        inventario()
    
    
    ss = input('desea salir?')
    if ss == 's':
        break






