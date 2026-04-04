from Conexion.conexion import get_connection

def crear_tablas():
    conn = get_connection()
    cursor = conn.cursor()

    # Crear tabla usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL
        );
    """)

    # Crear tabla reservas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id_reserva INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            telefono VARCHAR(20) NOT NULL,
            servicio VARCHAR(50) NOT NULL,
            fecha DATE NOT NULL,
            hora TIME NOT NULL
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Tablas creadas exitosamente.")

if __name__ == "__main__":
    crear_tablas()