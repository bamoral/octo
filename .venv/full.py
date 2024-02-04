import io
import sys
import requests

from UI import ui
from map_get import get_image

from PyQt5 import uic
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap, QImage, QColor, QTransform
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPushButton

SCREEN_SIZE = [1600, 900]

ui = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QPushButton" name="cords">
    <property name="geometry">
     <rect>
      <x>460</x>
      <y>60</y>
      <width>141</width>
      <height>23</height>
     </rect>
    </property>
    <property name="text">
     <string>Ввести координаты</string>
    </property>
   </widget>
   <widget class="QLabel" name="photo">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>220</y>
      <width>681</width>
      <height>291</height>
     </rect>
    </property>
    <property name="text">
     <string/>
    </property>
   </widget>
   <widget class="QLineEdit" name="coords">
    <property name="geometry">
     <rect>
      <x>90</x>
      <y>50</y>
      <width>301</width>
      <height>41</height>
     </rect>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


# 37.530887,55.703118
class MyPillow(QMainWindow):
    def __init__(self):
        self.anoth = 0
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.size >= 163.24:
                print('max')
            else:
                self.size = self.size * 2
                print(self.size)
                self.map_file = get_image(self.cordsnow, self.size)
                self.initUI()
        elif event.key() == Qt.Key_PageDown:  # Key_PageUp:
            if self.size <= 0.02:
                print('min')
            else:
                self.size = self.size / 2
                print(self.size)
                self.map_file = get_image(self.cordsnow, self.size)
                self.initUI()
        elif event.key() == Qt.Key_D:    # Key_PageUp:
            self.x = float(self.x) + float(self.size) / 10
            self.x = round(self.x, 5)
            print(self.x)
            self.cordsnow = f'{self.x},{self.y}'
            self.map_file = get_image(self.cordsnow, self.size)
            self.initUI()
        elif event.key() == Qt.Key_A:    # Key_PageUp:
            self.x = float(self.x) - float(self.size) / 10
            self.x = round(self.x, 5)
            print(self.x)
            self.cordsnow = f'{self.x},{self.y}'
            self.map_file = get_image(self.cordsnow, self.size)
            self.initUI()
        elif event.key() == Qt.Key_W:    # Key_PageUp:
            self.y = float(self.y) + float(self.size) / 10
            self.y = round(self.y, 5)
            print(self.y)
            self.cordsnow = f'{self.x},{self.y}'
            self.map_file = get_image(self.cordsnow, self.size)
            self.initUI()
        elif event.key() == Qt.Key_S:  # Key_PageUp:
            self.y = float(self.y) - float(self.size) / 10
            self.y = round(self.y, 5)
            print(self.y)
            self.cordsnow = f'{self.x},{self.y}'
            self.map_file = get_image(self.cordsnow, self.size)
            self.initUI()

        elif event.key() == Qt.Key_PageDown:    # Key_PageUp:
            pass

    def crd(self):
        # получаем координаты
        print('we are here')
        self.cordsnow = self.coords.text()
        data = str(self.cordsnow)
        data = data.split(',')
        self.x = data[0]
        self.y = data[1]
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

    def get_image(coords, size):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords}&spn={size},0.002&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        # возврааем картинку
        return map_file


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyPillow()
    ex.show()

    sys.exit(app.exec())