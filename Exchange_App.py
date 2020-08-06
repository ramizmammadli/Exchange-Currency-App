import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests
from bs4 import BeautifulSoup
import os
"""
İleri Seviye Modüller bölümünde yazdığımız döviz programı arayüz şeklinde yapmaya çalışın.
Bu sizi arayüz konusunda oldukça geliştirecektir.
"""


class Window(QWidget):
    def __init__(self):

        super().__init__()

        self.init_ui()

    def init_ui(self):

        self.show_currency = QPushButton("Show Currencies")
        self.exchange = QPushButton("Exchange")
        self.intro = QLabel()
        self.intro.setText("\tWelcome to the Exchange app!")
        self.intro.setFont(QFont('Times New Roman',14))
        self.author = QLabel()
        self.author.setText("\t\t\t\t\t\tRamiz Mammadli - 18011903")
        self.close_app = QPushButton("Close")

        v_box = QVBoxLayout()
        v_box.addWidget(self.intro)
        v_box.addStretch()
        v_box.addWidget(self.show_currency)
        v_box.addWidget(self.exchange)
        v_box.addWidget(self.close_app)
        v_box.addStretch()
        v_box.addWidget(self.author)


        h_box = QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        self.setWindowTitle("Exchange application")

        self.setLayout(h_box)
        self.setFixedHeight(900)
        self.setFixedWidth(1025)

        self.show_currency.clicked.connect(self.show_data)
        self.exchange.clicked.connect(self.do_exchange)
        self.close_app.clicked.connect(self.do_close)

        self.show()

    def do_close(self):
        self.close()

    def do_exchange(self):
        self.exchange_object = Exchange()
        self.exchange_object.show()
        self.hide()
    def show_data(self):
        self.currency_show = Show_Currency()
        self.currency_show.show()
        self.hide()


class Show_Currency(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.TakeData()

    def init_ui(self):

        self.caption = QLabel()
        self.caption.setText("Latest currencies:")
        self.caption.setFont(QFont('Times New Roman', 14))

        self.body = QLabel()
        self.body.setText(str(self.TakeData()))
        self.caption.setFont(QFont('Times New Roman', 12))

        v_box = QVBoxLayout()
        v_box.addWidget(self.caption)
        v_box.addWidget(self.body)

        self.setLayout(v_box)
        self.setFixedHeight(900)
        self.setFixedWidth(1025)

        self.show()


    def TakeData(self):
        url = "https://www.doviz.com/"

        response = requests.get(url)

        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        values = soup.find_all("span", {"class": "value"})
        data = []
        listname = ["Gold", "USD", "EUR", "EUR/USD", "GBP", "BIST 100", "Brand Petrolium", "Percentage"]
        count = 0
        try:
            for i in listname:
                data.append("{}. {} - {}".format(count + 1, listname[count], values[count].text))

                count += 1
        except (IndexError):  # error occured always. IDK why
            pass

        str = ""

        for i in data:
            str = str + i + "\n"


        return str

class Exchange(QWidget):
    def __init__(self):
        super().__init__()
        self.listname = ["Gold", "USD", "EUR", "EUR/USD", "GBP", "BIST 100", "Brand Petrolium", "Percentage"]
        self.TakeData()
        self.init_ui()

    def init_ui(self):
        self.calculate_button = QPushButton("Calculate")

        self.first = QLabel("First currency: ")
        self.second = QLabel("Second currency: ")
        self.first.setGeometry(40, 170, 191, 33)
        self.second.setGeometry(40, 250, 221, 33)
        self.comboBox_1 = QComboBox()
        self.comboBox_2 = QComboBox()
        self.result = QLabel("----------")
        self.data = self.TakeData()



        for i in self.listname:
            self.comboBox_1.addItem(i)
            self.comboBox_2.addItem(i)

        h_box = QHBoxLayout()
        h_box.addWidget(self.second)
        h_box.addWidget(self.comboBox_2)
        v_box = QVBoxLayout()
        v_box.addLayout(h_box)

        h_box2 = QHBoxLayout()
        h_box2.addWidget(self.first)
        h_box2.addWidget(self.comboBox_1)
        h_box2.addLayout(v_box)
        h_box2.addStretch()

        v_box2 = QVBoxLayout()
        v_box2.addStretch()
        v_box2.addLayout(h_box2)
        v_box2.addStretch()
        v_box2.addWidget(self.result)
        v_box2.addStretch()
        v_box2.addWidget(self.calculate_button)

        self.setLayout(v_box2)

        self.calculate_button.clicked.connect(self.do_calculate)


        self.setFixedHeight(900)
        self.setFixedWidth(1025)

    def TakeData(self):

        url = "https://www.doviz.com/"

        response = requests.get(url)

        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        values = soup.find_all("span", {"class": "value"})
        return values

    def do_calculate(self):

        first_cur = self.comboBox_1.currentText()
        second_cur = self.comboBox_2.currentText()
        for i, j in zip(self.listname, self.data):
            j = j.text
            j = str(j)
            j = j.replace(",", ".")
            j = j.replace("$", "")
            if (i == first_cur):
                value1 = float(j)
            elif (i == second_cur):
                value2 = float(j)

        self.result.setText("1 {} is equal to {} {}".format(second_cur, value2 / value1, first_cur))

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())