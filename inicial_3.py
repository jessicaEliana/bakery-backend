import os
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from app.models.product import Product
from app.database import init_app

d = os.path.dirname(__file__)
os.chdir(d)

ruta_destino = 'static/img'
if not os.path.exists(ruta_destino):
    os.makedirs(ruta_destino)

app = Flask(__name__)
CORS(app)
init_app(app)

@app.route('/')
def principal():
    return 'ya salioooooo ❤️'

@app.route('/products', methods=['POST'])
def upload_product():
    try:
        print("HOLI")
        data = request.form
        print("Request form data:", data)

        if 'imagen' not in request.files:
            return jsonify({'message': 'No se encontró el archivo de imagen'}), 400

        archivo = request.files['imagen']
        print(">>>>>>>>>>>>>>>>", data)
        print(">>>>>>>>>>>>>>>>", archivo)

        if archivo.filename == '':
            return jsonify({'message': 'No se seleccionó ningún archivo'}), 400

        nombre_imagen = secure_filename(archivo.filename)
        print(">>>>>>>>>>>>>>>>", nombre_imagen)

        nombre_base, extension = os.path.splitext(nombre_imagen)
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
        archivo.save(os.path.join(ruta_destino, nombre_imagen))

        required_fields = ['nombre_prod', 'precio_prod', 'stock_prod', 'descripcion_p']
        for field in required_fields:
            if field not in data:
                print(f"Campo {field} faltante en data: {data}")
                return jsonify({'message': f"Campo {field} faltante"}), 400

        new_prod = Product(
            nombre_prod=data['nombre_prod'],
            precio_prod=data['precio_prod'],
            stock_prod=data['stock_prod'],
            img_url=nombre_imagen,
            descripcion_p=data['descripcion_p']
        )
        new_prod.save()
        return jsonify({'message': 'Producto subido correctamente'}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Error al subir el producto', 'error': str(e)}), 500

@app.route('/products', methods=['GET'])
def get_all_prods():
    products = Product.get_all()
    productos_json = [prod.serialize() for prod in products]
    return jsonify(productos_json)

@app.route('/products/<int:id>', methods=['GET'])
def get_by_id_prod(id):
    product = Product.get_by_id(id)
    if product:
        return jsonify(product.serialize())
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_prod(id):
    product = Product.get_by_id(id)
    if not product:
        return jsonify({'message': 'Producto no encontrado'}), 404
    product.delete()
    return jsonify({'message': 'El producto fue borrado'})

@app.route('/products/<int:id>', methods=['PUT'])
def update_prod(id):
    product = Product.get_by_id(id)
    if not product:
        return jsonify({'message': 'Producto no encontrado'}), 404
    data = request.form
    product.nombre_prod = data.get('nombre_prod', product.nombre_prod)
    product.precio_prod = data.get('precio_prod', product.precio_prod)
    product.stock_prod = data.get('stock_prod', product.stock_prod)
    product.img_url = data.get('img_url', product.img_url)
    product.descripcion_p = data.get('descripcion_p', product.descripcion_p)
    product.save()
    return jsonify({'message': 'Producto actualizado correctamente'})


if __name__ == '__main__':
    app.run(debug=True)

