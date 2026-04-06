class Producto:
    def __init__(self, id_producto, nombre, precio, stock):
        self.id = id_producto
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

class Cliente:
    def __init__(self, id_cliente, nombre, telefono):
        self.id = id_cliente
        self.nombre = nombre
        self.telefono = telefono