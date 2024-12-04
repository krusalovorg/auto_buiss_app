import datetime

from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QComboBox, QLineEdit, QTextEdit, \
    QPushButton, QAbstractScrollArea, QHeaderView, QTabWidget, QWidget, QDateEdit
from PyQt6.QtGui import QColor
from PyQt6.uic.properties import QtWidgets, QtCore

from dialogs import ProductEditDialog, OrderDetailsDialog
from models import Order, Product, Client


class Tabs:
    def __init__(self, main_window):
        self.main_window = main_window

    def setup_commercial_tab(self, tab, clients, products, orders):
        layout = QVBoxLayout(tab)

        central_widget = QTabWidget()
        layout.addWidget(central_widget)

        orders_tab = QWidget()
        clients_tab = QWidget()

        central_widget.addTab(orders_tab, "Заказы")
        central_widget.addTab(clients_tab, "Клиенты")

        # Настройка таблицы заказов
        self.order_table = QTableWidget()
        self.order_table.setColumnCount(6)
        self.order_table.setHorizontalHeaderLabels(
            ["Дата регистрации", "Клиент", "Лесопродукция", "Количество", "Дата доставки", "Статус"]
        )
        self.order_table.verticalHeader().setDefaultSectionSize(22)
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        orders_layout = QVBoxLayout(orders_tab)
        orders_layout.addWidget(self.order_table)

        # Настройка таблицы клиентов
        self.client_table = QTableWidget()
        self.client_table.setColumnCount(2)
        self.client_table.setHorizontalHeaderLabels(["Имя клиента", "Контакты"])
        self.client_table.verticalHeader().setDefaultSectionSize(22)
        self.client_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        clients_layout = QVBoxLayout(clients_tab)
        clients_layout.addWidget(self.client_table)

        # Форма для добавления/редактирования клиентов
        self.client_name_input = QLineEdit()
        self.client_name_input.setPlaceholderText("Имя клиента")
        clients_layout.addWidget(self.client_name_input)

        self.client_contact_input = QLineEdit()
        self.client_contact_input.setPlaceholderText("Контакты клиента")
        clients_layout.addWidget(self.client_contact_input)

        self.client_confirm_button = QPushButton("Добавить/Сохранить клиента")
        self.client_confirm_button.clicked.connect(self.confirm_client)
        clients_layout.addWidget(self.client_confirm_button)

        self.update_client_table(clients)

        # Элементы управления для заказов
        self.client_input = QComboBox()
        for client in clients:
            self.client_input.addItem(client.name)
        orders_layout.addWidget(self.client_input)

        self.product_input = QComboBox()
        for product in products:
            self.product_input.addItem(product.name)
        orders_layout.addWidget(self.product_input)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Количество")
        orders_layout.addWidget(self.quantity_input)

        # self.delivery_date_input = QLineEdit()
        # self.delivery_date_input.setPlaceholderText("Дата доставки (YYYY-MM-DD)")
        # orders_layout.addWidget(self.delivery_date_input)

        self.delivery_date_input = QDateEdit()
        self.delivery_date_input.setCalendarPopup(True)
        self.delivery_date_input.setDateTime(QDateTime.currentDateTime())
        self.delivery_date_input.setWindowTitle("Дата доставки")
        orders_layout.addWidget(self.delivery_date_input)

        self.additional_info_input = QTextEdit()
        self.additional_info_input.setPlaceholderText("Дополнительная информация")
        orders_layout.addWidget(self.additional_info_input)

        self.confirm_button = QPushButton("Добавить/Сохранить заказ")
        self.confirm_button.clicked.connect(
            lambda: self.confirm_order()
        )
        orders_layout.addWidget(self.confirm_button)

        self.update_order_table(orders)

        self.editing_order_id = -1

        self.order_table.cellClicked.connect(self.auto_fill_edit_form)
        self.client_table.cellClicked.connect(self.auto_fill_client_form)

    def auto_fill_client_form(self, row, _):
        client = self.main_window.clients[row]
        self.client_name_input.setText(client.name)
        self.client_contact_input.setText(client.contact)
        self.editing_client_id = row

    def update_client_table(self, clients):
        self.client_table.setRowCount(len(clients))
        for row, client in enumerate(clients):
            self.client_table.setItem(row, 0, QTableWidgetItem(client.name))
            self.client_table.setItem(row, 1, QTableWidgetItem(client.contact))

    def confirm_client(self):
        name = self.client_name_input.text()
        contact = self.client_contact_input.text()

        if name and contact:
            if hasattr(self, 'editing_client_id') and self.editing_client_id > -1:
                # Редактирование существующего клиента
                client = self.main_window.clients[self.editing_client_id]
                client.name = name
                client.contact = contact
                self.main_window.clients[self.editing_client_id] = client
                self.editing_client_id = -1
            else:
                new_client = Client(name=name, contact=contact)
                self.main_window.clients.append(new_client)

            self.client_input.clear()
            for client in self.main_window.clients:
                self.client_input.addItem(client.name)
            self.update_order_table(self.main_window.orders)
            self.update_client_table(self.main_window.clients)
            self.client_name_input.clear()
            self.client_contact_input.clear()

    def auto_fill_edit_form(self, row, _):
        # Автозаполнение формы при клике на заказ
        order = self.main_window.orders[row]
        self.client_input.setCurrentText(order.client.name)
        self.product_input.setCurrentText(order.product.name)
        self.quantity_input.setText(str(order.quantity))
        self.delivery_date_input.setDateTime(datetime.datetime.strptime(order.delivery_date, "%d.%m.%y"))
        self.additional_info_input.setText(order.additional_info)
        self.editing_order_id = row

    def confirm_order(self):
        # Сохранение изменений или добавление нового заказа
        client_name = self.main_window.clients[self.client_input.currentIndex()]
        product_name = self.main_window.products[self.product_input.currentIndex()]
        quantity = self.quantity_input.text()
        delivery_date = self.delivery_date_input.text()
        additional_info = self.additional_info_input.toPlainText()

        if client_name and product_name:
            if self.editing_order_id > -1:
                order = self.main_window.orders[self.editing_order_id]
                order.client = client_name
                order.product = product_name
                order.quantity = int(quantity)
                order.delivery_date = delivery_date
                order.additional_info = additional_info
                self.main_window.orders[self.editing_order_id] = order
                self.editing_order_id = -1
                self.quantity_input.clear()
                self.delivery_date_input.clear()
                self.additional_info_input.clear()
            else:
                new_order = Order(
                    client=client_name,
                    product=product_name,
                    quantity=int(quantity),
                    delivery_date=delivery_date,
                    additional_info=additional_info,
                )
                if new_order.can_confirm():
                    self.main_window.orders.append(new_order)

            self.update_order_table(self.main_window.orders)

    def view_order_details(self, row, _):
        order = self.main_window.orders[row]
        dialog = OrderDetailsDialog(order, self.production_table)
        dialog.exec()

    def setup_production_tab(self, tab, orders):
        layout = QVBoxLayout(tab)
        label = QLabel("Список заказов для производства")
        layout.addWidget(label)

        self.production_table = QTableWidget()
        self.production_table.setColumnCount(6)
        self.production_table.setHorizontalHeaderLabels(
            ["Дата регистрации", "Клиент", "Лесопродукция", "Количество", "Дата доставки", "Статус"]
        )
        self.production_table.resizeColumnsToContents()
        layout.addWidget(self.production_table)

        self.production_table.verticalHeader().setDefaultSectionSize(22)
        self.production_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.update_order_table(orders)

    def setup_technologist_tab(self, tab, products):
        layout = QVBoxLayout(tab)
        label = QLabel("Информация о видах лесопродукции")
        layout.addWidget(label)

        self.product_table = QTableWidget()
        self.product_table.setColumnCount(1)
        self.product_table.setHorizontalHeaderLabels(["Название лесопродукции"])
        self.product_table.setRowCount(len(products))
        self.product_table.verticalHeader().setDefaultSectionSize(22)
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for row, product in enumerate(products):
            self.product_table.setItem(row, 0, QTableWidgetItem(product.name))
        layout.addWidget(self.product_table)
        self.product_table.cellDoubleClicked.connect(self.edit_product)

        name_product = QLineEdit()
        name_product.setPlaceholderText("Название продукции")
        layout.addWidget(name_product)

        confirm_button = QPushButton("Добавить")
        confirm_button.clicked.connect(
            lambda: self.onAddProductTech(name_product)
        )
        layout.addWidget(confirm_button)

    def onAddProductTech(self, name_input):
        if name_input.text():
            self.main_window.products.append(Product(name_input.text()))
            name_input.clear()

            self.product_table.setRowCount(len(self.main_window.products))
            for row, product in enumerate(self.main_window.products):
                self.product_table.setItem(row, 0, QTableWidgetItem(product.name))
            self.update_form_add_order()

    def update_form_add_order(self):
        self.product_input.clear()
        for product in self.main_window.products:
            self.product_input.addItem(product.name)

    def edit_product(self, row, _):
        product = self.main_window.products[row]
        dialog = ProductEditDialog(product, self.main_window)
        if dialog.exec():
            self.product_table.setItem(row, 0, QTableWidgetItem(product.name))

    def update_order_table(self, orders):
        self.order_table.setRowCount(len(orders))
        for row, order in enumerate(orders):
            self.order_table.setItem(row, 0, QTableWidgetItem(order.registration_date))
            self.order_table.setItem(row, 1, QTableWidgetItem(order.client.name))
            self.order_table.setItem(row, 2, QTableWidgetItem(order.product.name))
            self.order_table.setItem(row, 3, QTableWidgetItem(str(order.quantity)))
            self.order_table.setItem(row, 4, QTableWidgetItem(order.delivery_date))
            self.order_table.setItem(row, 5, QTableWidgetItem(order.status))

            if order.status == "Согласован клиентом":
                color = QColor(255, 165, 0)
            elif order.status == "Принят в производство":
                color = QColor(255, 255, 0)
            elif order.status == "Выполнен":
                color = QColor(0, 255, 0)
            else:
                color = QColor(211, 211, 211)
            self.order_table.item(row, 5).setBackground(color)
