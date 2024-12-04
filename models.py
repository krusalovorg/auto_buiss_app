import time
from datetime import datetime

class Product:
    def __init__(self, name):
        self.name = name


class Client:
    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

    def __str__(self):
        return f"Client(name={self.name}, contact={self.contact})"

    def can_confirm(self):
        # Здесь можно добавить проверку, что клиент имеет валидные данные
        return bool(self.name and self.contact)

    def update_info(self, name=None, contact=None):
        if name:
            self.name = name
        if contact:
            self.contact = contact

class Order:
    STATUSES = ["Черновик", "Согласован клиентом", "Принят в производство", "Выполнен"]

    def __init__(self, client: Client, product, quantity, delivery_date, additional_info):
        self.registration_date = datetime.now().strftime("%d.%m.%Y")
        self.id = time.time()
        self.client = client
        self.product = product
        self.quantity = quantity
        self.delivery_date = delivery_date
        self.additional_info = additional_info
        self.status = "Черновик"

    def can_confirm(self):
        if self.client and self.product and self.delivery_date and self.quantity > 0:
            self.status = self.STATUSES[1]
            return True
        elif self.client and (self.product or self.quantity > 0 or self.delivery_date):
            self.status = self.STATUSES[0]
            return True
        return False