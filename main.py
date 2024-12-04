import sys
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QApplication
from models import Product, Client, Order
from tabs import Tabs


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лесозавод №10 Белка")
        self.setGeometry(100, 100, 1000, 700)

        self.products = [
            Product("Сырые пиломатериалы"),
            Product("Сухие пиломатериалы"),
            Product("Рейки"),
            Product("Клееный брус"),
            Product("Фанера"),
            Product("Доска пола"),
        ]
        self.clients = [Client("ООО \'НикоТурс Тольятти\'", "nikotuors"), Client("Клиент 2", "+89998887766")]
        self.orders = [
            Order(self.clients[0], self.products[0], 50, "01.12.2024", "Срочно"),
            Order(self.clients[1], self.products[1], 30, "10.12.2024", "Требуется доставка"),
        ]

        for order in self.orders:
            order.status = "Согласован клиентом"

        self.init_ui()

    def init_ui(self):
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        self.commercial_tab = QWidget()
        self.production_tab = QWidget()
        self.technologist_tab = QWidget()

        self.central_widget.addTab(self.commercial_tab, "Коммерческая служба")
        self.central_widget.addTab(self.production_tab, "Служба производства")
        self.central_widget.addTab(self.technologist_tab, "Служба технолога")

        tabs = Tabs(self)
        tabs.setup_commercial_tab(self.commercial_tab, self.clients, self.products, self.orders)
        tabs.setup_production_tab(self.production_tab, self.orders)
        tabs.setup_technologist_tab(self.technologist_tab, self.products)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
