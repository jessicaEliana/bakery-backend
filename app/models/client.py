class Client:
    def __init__(self, id_cl, nombre_cl, tel_cl=None, dni_cl=None):
        self.id_cl = id_cl
        self.nombre_cl = nombre_cl
        self.tel_cl = tel_cl
        self.dni_cl = dni_cl
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def __repr__(self):
        return f'<Client {self.nombre_cl}>'