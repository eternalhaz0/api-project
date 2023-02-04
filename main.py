import os
import sys

import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow

SCREEN_SIZE = [600, 450]


class StaticMap(QMainWindow):
    current_LL = (37.530887, 55.703118)
    current_spn = (0.002, 0.002)
    current_map_type = 'map'

    map_api_server = "http://static-maps.yandex.ru/1.x/"

    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        map_params = {
            "ll": ",".join(map(str, self.current_LL)),
            "spn": ",".join(map(str, self.current_spn)),
            "l": self.current_map_type
        }
        response = requests.get(self.map_api_server, map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(self.map_api_server)
            print("Http статус:", response.status_code, "(", response.reason, ")")

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        uic.loadUi('ui\main_window.ui', self)  # Загружаем дизайн

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StaticMap()
    ex.show()
    sys.exit(app.exec())
