# inventario/inventario.py

import os

class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def to_line(self):
        """Convierte el producto en una línea de texto para guardar en TXT"""
        return f"{self.id},{self.nombre},{self.cantidad},{self.precio}\n"

    @staticmethod
    def from_line(linea):
        """Crea un objeto Producto desde una línea de texto"""
        id, nombre, cantidad, precio = linea.strip().split(",")
        return Producto(int(id), nombre, int(cantidad), float(precio))


class Inventario:
    def __init__(self, archivo_path):
        self.archivo_path = archivo_path
        self.productos = self.cargar_productos()

    def cargar_productos(self):
        productos = []
        if os.path.exists(self.archivo_path):
            with open(self.archivo_path, "r", encoding="utf-8") as f:
                for linea in f:
                    if linea.strip():
                        productos.append(Producto.from_line(linea))
        return productos

    def guardar_productos(self):
        with open(self.archivo_path, "w", encoding="utf-8") as f:
            for prod in self.productos:
                f.write(prod.to_line())

    def agregar_producto(self, producto):
        self.productos.append(producto)
        self.guardar_productos()

    def obtener_siguiente_id(self):
        if not self.productos:
            return 1
        return max(p.id for p in self.productos) + 1
    