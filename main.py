import os
import sys

import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QWheelEvent
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5 import QtCore

SCREEN_SIZE = [600, 450]


class StaticMap(QMainWindow):
    current_LL = (37.530887, 55.703118)
    current_spn = (0.002, 0.002)
    current_map_type = 'map'

    map_api_server = "http://static-maps.yandex.ru/1.x/"

    def __init__(self):
        super().__init__()
        self.initUI()
        self.getImage()

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
        uic.loadUi('static_map.ui', self)  # Загружаем дизайн

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.angleDelta().y() > 0:
            self.changeMapScale('-')
        else:
            self.changeMapScale('+')
        self.getImage()

    def changeMapScale(self, eventScaleType: str):
        current_change = 1
        if eventScaleType == '-':
            current_change = -current_change
        new_spn = (self.current_spn[0] + current_change, self.current_spn[1] + current_change)
        if 0 <= new_spn[0] <= 90 and 0 <= new_spn[1] <= 90:
            self.current_spn = new_spn
     
    def changeMapCenterPoint(self, event_change_type: str):
        current_change = 1
        current_delta = None
        if event_change_type == 'up':
            current_delta = (0, 1)
        new_LL = (self.current_LL[0] + current_delta[0], self.current_LL[1] + current_delta[1])
        if 0 <= new_LL[0] <= 90 and 0 <= new_LL[1] <= 180:
            self.current_LL = new_LL

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Up:
            self.changeMapCenterPoint('up')
        self.getImage()
        
    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StaticMap()
    ex.show()
    sys.exit(app.exec())
