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

# Guardar en TXT (simple línea por producto)
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
            