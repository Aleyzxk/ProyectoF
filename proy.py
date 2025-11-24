import os, json

#programa de colas de pedidos y almacenamiento de productos.
import json

def guardar_datos(inventario, cola, archivo="datos.json"):
    data = {
        "inventario": [],
        "cola": []
    }

    # Guardar inventario
    for slot in inventario.slots:
        if slot is not None and slot != inventario._deleted:
            data["inventario"].append({
                "key": slot.key,
                "value": slot.value,
                "cant": slot.cant
            })

    # Guardar cola
    actual = cola.head
    while actual is not None:
        ped = actual.data
        data["cola"].append({
            "id": ped.id,
            "solicitante": ped.solicitante,
            "producto": ped.producto
        })
        actual = actual.next

    with open(archivo, "w") as f:
        json.dump(data, f, indent=4)

    print(" Datos guardados.")
    
def cargar_datos(inventario, cola, archivo="datos.json"):
    if not os.path.exists(archivo):
        return  

    with open(archivo, "r") as f:
        data = json.load(f)

    # Cargar inventario
    for item in data["inventario"]:
        inventario.put(item["key"], item["value"], item["cant"])

    # Cargar cola
    for p in data["cola"]:
        nuevo = pedido(p["solicitante"], p["producto"])
        nuevo.id = p["id"]  # conservar ID original
        cola.enqueue(nuevo)

    # Ajustar el contador de IDs
    if data["cola"]:
        pedido._contador_id = max(p["id"] for p in data["cola"]) + 1

    
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
        h = self._hash(key)
        while self.slots[h] is not None:
            if self.slots[h] != self._deleted and self.slots[h].key == key:
                return self.slots[h]
            h = (h + 1) % self.size
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

class queue:
    def __init__(self, inventario):
        self.head = None
        self.tail = None
        self.count = 0
        self.inventario = inventario
        
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
    def show_queue(self):
        if self.head is None:
            print("La cola está vacía.")
            return

        print("Contenido de la cola:")
        actual = self.head
        while actual is not None:
            print(actual.data)   # mostrar el dato del nodo
            actual = actual.next
            
    def ant_dequeue(self):
        nombre = input("nombre: ")
        producto = input('producto: ')
        
        item = self.inventario.get(producto)
        
        if item is None:
            print("el producto no existe en el inventario")
            return
        if int(item.cant) <= 0:
            print('no hay stock disponible')
            return
        
        newpedido = pedido(nombre, producto)
        self.enqueue(newpedido)
        
        item.cant = str(int(item.cant) - 1)
        
        
        
class pedido:
    _contador_id = 1
    
    def __init__(self, solicitante, producto):
        self.id = pedido._contador_id
        pedido._contador_id += 1

        self.solicitante = solicitante
        self.producto = producto
        
        
    def __str__(self):
        return f"Pedido #{self.id} - {self.solicitante} pidió {self.producto}"
    
        

        
def inventario():
    inv.show_all()
    resp = int(input('que deseas hacer? \n 1. Insertar \n 2. Eliminar \n 3. regresar \n'))
    if resp == 1:
        inv.put_interactivo()
    elif resp == 2:
        inv.delete_inter()
    else:
        return
        
        
def colaa():
    cola.show_queue()
    resp = int(input('que deseas hacer? \n 1. insertar? \n 2. tomar el pedido \n 3. regresar \n' ))
    if resp == 1:
        cola.ant_dequeue()
    elif resp == 2:
        nodo = cola.dequeue()
        print(f'pedido tomado y eliminado de la cola: \n {nodo.data}\n')
    else:
        return
    

inv = HashTable()
cola = queue(inv)

cargar_datos(inv, cola)

while True:
    #el menu del programa
    os.system('cls')
    print("sistema de cola de pedidos e inventario")
    print('que desea hacer?')
    print('1. ver inventario:')
    print('2. ver cola')
    print('3. salir')
    resp = int(input())
    
    if resp == 1:
        inventario()
    elif resp == 2:
        colaa()
    elif resp == 3:
        guardar_datos(inv,cola)
        break


