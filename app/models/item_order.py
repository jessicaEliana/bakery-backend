class ItemOrder:
    def __init__(self, id_item, order, product, cant_i, precio_i):
        self.id_item = id_item
        self.order = order
        self.product = product
        self.cant_i = cant_i
        self.precio_i = precio_i

    def __repr__(self):
        return f'<ItemOrder {self.id_item}>'
    
    