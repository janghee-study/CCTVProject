import sys
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

form_class = uic.loadUiType("pixmapTest.ui")[0]

class WindowClass(QMainWindow, form_class):
    cnt=0
    def __init__(self) :

        super().__init__()
        self.setupUi(self)

        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load("target.jpg")
        self.label.setPixmap(self.qPixmapFileVar)
        # 버튼에 기능을 연결하는 코드
        self.start.clicked.connect(self.button1Function)

    # btn_1이 눌리면 작동할 함수
    def button1Function(self):
        self.qPixmapFileVar.load("thumbnail0.png")
        self.label.setPixmap(self.qPixmapFileVar)
        print("얼굴인식을 시작하겠씁니다")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()