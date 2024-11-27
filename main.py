import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QTableWidget, QTableWidgetItem,
                             QPushButton, QLineEdit, QComboBox, QTextEdit)
from datetime import datetime

class Product:
    def __init__(self, name):
        self.name = name

class Client:
    def __init__(self, name):
        self.name = name

class Order:
    STATUSES = ["Черновик", "Согласован клиентом", "Принят в производство", "Выполнен"]

    def __init__(self, client, product, quantity, delivery_date, additional_info):
        self.registration_date = datetime.now()
        self.client = client
        self.product = product
        self.quantity = quantity
        self.delivery_date = delivery_date
        self.additional_info = additional_info
        self.status = "Черновик"

    def can_confirm(self):
        return self.status == "Черновик" and self.client and self.product and self.quantity > 0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лесозавод №10 Белка")
        self.setGeometry(100, 100, 800, 600)

        self.products = [Product("Сырые пиломатериалы"), Product("Сухие пиломатериалы"),
                         Product("Рейк"), Product("Клееный брус"), Product("Фанера"), Product("Доска пола")]
        self.clients = [Client("Клиент 1"), Client("Клиент 2")]
        self.orders = []

        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(6)
        self.order_table.setHorizontalHeaderLabels(
            ["Дата регистрации", "Клиент", "Лесопродукция", "Количество", "Дата доставки", "Статус"])
        layout.addWidget(self.order_table)

        self.client_input = QComboBox()
        for client in self.clients:
            self.client_input.addItem(client.name)
        layout.addWidget(self.client_input)

        self.product_input = QComboBox()
        for product in self.products:
            self.product_input.addItem(product.name)
        layout.addWidget(self.product_input)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Количество")
        layout.addWidget(self.quantity_input)

        self.delivery_date_input = QLineEdit()
        self.delivery_date_input.setPlaceholderText("Дата доставки (YYYY-MM-DD)")
        layout.addWidget(self.delivery_date_input)

        self.additional_info_input = QTextEdit()
        self.additional_info_input.setPlaceholderText("Дополнительная информация")
        layout.addWidget(self.additional_info_input)

        self.confirm_button = QPushButton("Согласовать заказ")
        self.confirm_button.clicked.connect(self.confirm_order)
        layout.addWidget(self.confirm_button)

    def confirm_order(self):
        client = self.clients[self.client_input.currentIndex()]
        product = self.products[self.product_input.currentIndex()]
        quantity = int(self.quantity_input.text())
        delivery_date = self.delivery_date_input.text()
        additional_info = self.additional_info_input.toPlainText()

        order = Order(client, product, quantity, delivery_date, additional_info)
        if order.can_confirm():
            order.status = "Согласован клиентом"
            self.orders.append(order)
            self.update_order_table()

    def update_order_table(self):
        self.order_table.setRowCount(len(self.orders))
        for row, order in enumerate(self.orders):
            self.order_table.setItem(row, 0, QTableWidgetItem(order.registration_date.strftime("%Y-%m-%d")))
            self.order_table.setItem(row, 1, QTableWidgetItem(order.client.name))
            self.order_table.setItem(row, 2, QTableWidgetItem(order.product.name))
            self.order_table.setItem(row, 3, QTableWidgetItem(str(order.quantity)))
            self.order_table.setItem(row, 4, QTableWidgetItem(order.delivery_date))
            self.order_table.setItem(row, 5, QTableWidgetItem(order.status))

            # Цветовое выделение в зависимости от статуса
            if order.status == "Согласован клиентом":
                self.order_table.item(row, 5).setBackgroundColor((255, 165, 0))  # Оранжевый
            elif order.status == "Принят в производство":
                self.order_table.item(row, 5).setBackgroundColor((255, 255, 0))  # Желтый
            elif order.status == "Выполнен":
                self.order_table.item(row, 5).setBackgroundColor((0, 255, 0))  # Зеленый

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())