import mysql.connector

from app.database import get_db

class Order:
    def __init__(self, nro_pdido, fecha_pdido, client):
        self.nro_pdido = nro_pdido
        self.fecha_pdido = fecha_pdido
        self.client = client
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def verify_client(self):
        db = get_db
        cursor = db.cursor()
        cursor.execute("SELECT id_cl FROM clientes WHERE id_cl = %s", (self.client.id_cl,))
        result = cursor.fetchone()
        cursor.close()
        
        return result is not None

    def insert_order(self):
        db = get_db
        cursor = db.cursor()

        try:
            # Verificar si el cliente existe en la base de datos
            if not self.verify_client():
                # Si el cliente no existe, insertar el cliente
                cursor.execute(
                    "INSERT INTO clientes (id_cl, nombre_cl, tel_cl, dni_cl) VALUES (%s, %s, %s, %s)",
                    (self.client.id_cl, self.client.nombre_cl, self.client.tel_cl, self.client.dni_cl)
                )

            # Insertar el pedido
            cursor.execute(
                "INSERT INTO pedidos (fecha_pdido, id_cl) VALUES (%s, %s)",
                (self.fecha_pdido, self.client.id_cl)
            )

            # Obtener el ID del pedido recién insertado
            order_id = cursor.lastrowid

            # Insertar los ítems del pedido
            for item in self.items:
                cursor.execute(
                    "INSERT INTO itemspedidos (nro_pdido, id_p, cant_i, precio_i) VALUES (%s, %s, %s, %s)",
                    (order_id, item.product.id_p, item.cant_i, item.precio_i)
                )

            # Confirmar transacción
            db.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            db.rollback()

        finally:
            cursor.close()
            

        print(f'Order {order_id} inserted successfully')

    def __repr__(self):
        return f'<Order {self.nro_pdido}>'
    
    # Método para representar la instancia de la clase Order como una cadena
    def __str__(self):
        return f'Pedido: {self.nro_pdido} - Cliente: {self.client} - Fecha: {self.fecha_pdido}'