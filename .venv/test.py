import io
import sys
import requests

from UI import ui
from map_get import get_image

from PyQt5 import uic
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap, QImage, QColor, QTransform
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel

SCREEN_SIZE = [1600, 900]


class MyPillow(QMainWindow):
    def __init__(self):
        super(MyPillow, self).__init__()
        # загружаем ui
        f = io.StringIO(ui)
        uic.loadUi(f, self)
        # подключаем кнопки
        self.cords.clicked.connect(self.crd)
        self.size = 0.02
        self.image = QLabel(self)
        self.image.move(100, 130)
        self.image.resize(600, 450)

    def crd(self):
        # получаем координаты
        print('we are here')
        self.cordsnow = self.coords.text()
        print(self.cordsnow)
        # получаем изображение
        self.map_file = get_image(self.cordsnow, self.size)
        # подгружаем картинку
        self.initUI()

    def initUI(self):
        # Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyPillow()
    ex.show()

    sys.exit(app.exec())