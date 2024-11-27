from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt
from models import Order, Product


class ProductEditDialog(QDialog):
    def __init__(self, product: Product, parent=None):
        super().__init__(parent)
        self.product = product
        self.setWindowTitle("Редактирование продукта")
        self.setLayout(QVBoxLayout())

        self.name_input = QLineEdit(self.product.name)
        self.layout().addWidget(QLabel("Название продукта:"))
        self.layout().addWidget(self.name_input)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_product)
        self.layout().addWidget(self.save_button)

    def save_product(self):
        self.product.name = self.name_input.text()
        self.accept()


class OrderDetailsDialog(QDialog):
    def __init__(self, order: Order, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Детали заказа")
        self.setLayout(QVBoxLayout())

        self.layout().addWidget(QLabel(f"Клиент: {order.client.name}"))
        self.layout().addWidget(QLabel(f"Продукт: {order.product.name}"))
        self.layout().addWidget(QLabel(f"Количество: {order.quantity}"))
        self.layout().addWidget(QLabel(f"Дата регистрации: {order.registration_date.strftime('%Y-%m-%d')}"))
        self.layout().addWidget(QLabel(f"Дата доставки: {order.delivery_date}"))
        self.layout().addWidget(QLabel(f"Статус: {order.status}"))
        self.layout().addWidget(QLabel(f"Доп. информация: {order.additional_info}"))

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.accept)
        self.layout().addWidget(close_button)
