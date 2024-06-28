from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

print(">>>>>>>>>>>>>>>", __name__)
class Productos:
    def __init__(self, id_productos, nombre_prod, precio_prod, stock_prod, descripcion_p):
        self.id_productos = id_productos
        self.nombre_prod = nombre_prod
        self.precio_prod = precio_prod
        self.stock_prod = stock_prod
        self.descripcion_p = descripcion_p

productos = [
    Productos(1,'Torta de Chocolate',24000.00,2,'Deliciosa torta de chocolate hecha con cacao puro y decorada con ganache de chocolate'),
    Productos(2,'Torta de Zanahoria',25500.00,3,'Elegante torta de terciopelo rojo con capas de queso crema, ideal para celebraciones especiales'),
    Productos(3,'Cheesecake de Frutos Rojos',15000.00,3,'Suave tarta de queso con base de galleta, cubierto con una capa de frutos rojos fresco')    
    ]

# print(productos)

@app.route('/')
def principal():
    return 'ya va saliendo  ❤️❤️❤️❤️❤️❤️'


@app.route('/products', methods=['GET'])
def get_products():
    """ recupera todos los productos de la lista de ejemplo """
    list_products = []

    for product in productos:
        list_products.append({
            'id_productos': product.id_productos,
            'nombre_prod': product.nombre_prod,
            'precio_prod': product.precio_prod,
            'stock_prod': product.stock_prod,
            'descripcion_p': product.descripcion_p
        })

    return jsonify(list_products)

if __name__ == '__main__':
    app.run(debug=True)