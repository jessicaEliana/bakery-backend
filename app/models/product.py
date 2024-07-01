from app.models.order import Order

from app.database import get_db

class Product:
    # Constructor de la clase Product
    def __init__(self, id_prod=None, nombre_prod=None, precio_prod=None, stock_prod=None, img_url=None, descripcion_p=None):
        self.id_prod = id_prod # ID del producto
        self.nombre_prod = nombre_prod # Nombre del producto
        self.precio_prod = precio_prod # Precio del producto
        self.stock_prod = stock_prod    # Stock del producto
        self.img_url = img_url    # URL de la imagen del producto
        self.descripcion_p = descripcion_p # Descripción del producto
        
    
    # Método para guardar o actualizar un producto en la base de datos
    def save(self):
        db=get_db()
        cursor=db.cursor()
        if self.id_prod is None:
            # Si el ID del producto no existe, insertarlo
            sql='INSERT INTO productos (nombre_prod, precio_prod,stock_prod,img_url,descripcion_p) VALUES (%s,%s,%s,%s,%s)'
            values=(self.nombre_prod,self.precio_prod,self.stock_prod, self.img_url,self.descripcion_p)
            cursor.execute(sql,values)
            self.id_prod=cursor.lastrowid
        else:
            # Si el ID del producto ya existe, actualizarlo
            sql='UPDATE productos SET nombre_prod=%s, precio_prod=%s,stock_prod=%s,img_url=%s,descripcion_p=%s WHERE id_prod=%s'
            values=(self.nombre_prod,self.precio_prod,self.stock_prod,self.img_url,self.descripcion_p,self.id_prod)
            cursor.execute(sql,values)
        db.commit()
        cursor.close()
        
    
    # Método estatico para obtener todos los productos de la base de datos
    @staticmethod
    def get_all():
        db=get_db()
        cursor=db.cursor()
        cursor.execute('SELECT * FROM productos')
        result=cursor.fetchall()
        products_dict={}

        for row in result:
            id_prod=row[0]
            if id_prod not in products_dict:
                products_dict[id_prod]=Product(id_prod=row[0],nombre_prod=row[1],precio_prod=row[2],stock_prod=row[3],img_url=row[4], descripcion_p=row[5])

        db.commit()
        cursor.close()
        return list(products_dict.values())  # Devolver la lista de productos
    
    # Método para obtener un producto de la base de datos

    @staticmethod
    def get_by_id(id_prod):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT
                p.id_prod, p.nombre_prod, p.precio_prod, p.stock_prod, p.img_url, p.descripcion_p
            FROM
                productos p
            WHERE
                p.id_prod = %s
            """, (id_prod,))
        
        rows = cursor.fetchall()
        cursor.close()

        if rows:
            prod_map = {}
            for row in rows:
                if row[0] not in prod_map:
                    prod_map[row[0]] = Product(id_prod=row[0], nombre_prod=row[1], precio_prod=row[2], stock_prod=row[3], img_url=row[4], descripcion_p=row[5])
            
            if id_prod in prod_map:
                return prod_map[id_prod]
            else:
                return None  # Si no se encuentra el producto con ese ID

        return None  # Si no se encontró ningún producto



    # @staticmethod
    # def get_by_id(id_prod):
    #     db=get_db()
    #     cursor=db.cursor()
    #     cursor.execute("""
    #         SELECT
    #             p.id_prod, p.nombre_prod, p.precio_prod, p.stock_prod, p.img_url, p.descripcion_p
    #         FROM
    #             productos p
    #         WHERE
    #             p.id_prod = %s
    #         """, (id_prod,))
        # result=cursor.fetchone()
        # if result is not None:
        #     return Product(id_prod=result[0], nombre_prod=result[1], precio_prod=result[2], stock_prod=result[3], descripcion_p=result[4])
        # else:
        #     return None

        rows = cursor.fetchall()
        cursor.close()

        if rows:
            # Utilizamos un diccionario para mapear los productos por su ID para evitar duplicados
            prod_map = {}
            for row in rows:
                if row[0] not in prod_map:
                    prod_map[row[0]] = Product(id_prod=row[0], nombre_prod=row[1], precio_prod=row[2], stock_prod=row[3], img_url=row[4], descripcion_p=row[5])
                
            return prod_map[id_prod]

        return None # Si no encontré el producto devolver None

        # cursor.execute('SELECT * FROM productos WHERE id_prod=%s', (id_prod,))
        # result=cursor.fetchone()
        # return Product(id_prod=result[0], nombre_prod=result[1], precio_prod=result[2], stock_prod=result[3], descripcion_p=result[4])
    
    # Método para eliminar un producto de la base de datos
    def delete(self):
        db=get_db()
        cursor=db.cursor()
        sql='DELETE FROM productos WHERE id_prod=%s'
        values=(self.id_prod,)
        cursor.execute(sql,values)
        db.commit()

    # Método para serializar un objeto Product a un diccionario
    def serialize(self):
        return {
            'id_prod': self.id_prod,
            'nombre_prod': self.nombre_prod,
            'precio_prod': self.precio_prod,
            'stock_prod': self.stock_prod,
            'img_url': self.img_url,
            'descripcion_p': self.descripcion_p,
        }
    
    def __str__(self):
        return f'ID: {self.id_prod}, Nombre: {self.nombre_prod}, Precio: {self.precio_prod}, Stock: {self.stock_prod}, Descripción: {self.descripcion_p}'