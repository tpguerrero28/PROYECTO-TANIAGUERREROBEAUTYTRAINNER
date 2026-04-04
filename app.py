# inventario/inventario.py

import json
import csv
import os

# Clase Producto
class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def to_dict(self):
        """Convierte el producto en diccionario para JSON/CSV"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

# Clase Inventario
class Inventario:
    def __init__(self):
        self.productos = {}  # Diccionario con id como clave

    def agregar_producto(self, producto):
        self.productos[producto.id] = producto

    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]

    def actualizar_producto(self, id_producto, nombre=None, cantidad=None, precio=None):
        if id_producto in self.productos:
            p = self.productos[id_producto]
            if nombre is not None: p.nombre = nombre
            if cantidad is not None: p.cantidad = cantidad
            if precio is not None: p.precio = precio

    def listar_productos(self):
        return list(self.productos.values())

    # Guardar en JSON
    def guardar_json(self, archivo):
        data = [p.to_dict() for p in self.productos.values()]
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    # Leer desde JSON
    def cargar_json(self, archivo):
        if not os.path.exists(archivo):
            return
        with open(archivo, "r", encoding="utf-8") as f:
            data = json.load(f)
            for p in data:
                producto = Producto(p["id"], p["nombre"], p["cantidad"], p["precio"])
                self.agregar_producto(producto)

    # Guardar en CSV
    def guardar_csv(self, archivo):
        with open(archivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id","nombre","cantidad","precio"])
            writer.writeheader()
            for p in self.productos.values():
                writer.writerow(p.to_dict())

    # Leer desde CSV
    def cargar_csv(self, archivo):
        if not os.path.exists(archivo):
            return
        with open(archivo, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                producto = Producto(int(row["id"]), row["nombre"], int(row["cantidad"]), float(row["precio"]))
                self.agregar_producto(producto)

    # Guardar en TXT
    def guardar_txt(self, archivo):
        with open(archivo, "w", encoding="utf-8") as f:
            for p in self.productos.values():
                f.write(f"{p.id},{p.nombre},{p.cantidad},{p.precio}\n")

    # Leer desde TXT
    def cargar_txt(self, archivo):
        if not os.path.exists(archivo):
            return
        with open(archivo, "r", encoding="utf-8") as f:
            for line in f:
                id_, nombre, cantidad, precio = line.strip().split(",")
                producto = Producto(int(id_), nombre, int(cantidad), float(precio))
                self.agregar_producto(producto)
                