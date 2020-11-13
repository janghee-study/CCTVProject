import sys
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import cv2
import threading
import time
import os

cnt = 0
running = False


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(self.createFirstExclusiveGroup(), 0, 0)
        grid.addWidget(self.createSecondExclusiveGroup(), 1, 0)
        grid.addWidget(self.createNonExclusiveGroup(), 0, 1)
        grid.addWidget(self.webcam(), 1, 1)
        self.setLayout(grid)
        self.setWindowTitle('영상처리')
        self.setGeometry(300, 100, 1400, 800)
        app.aboutToQuit.connect(self.onExit)
        self.show()

    def createFirstExclusiveGroup(self):
        groupbox = QGroupBox('GIF보는부분')
        self.movie = QMovie("CCTV.jpg", QByteArray(), self)
        size = self.movie.scaledSize() / 2
        self.setGeometry(0, 0, size.width(), size.height())
        self.setWindowTitle("GIF")
        self.movie_screen = QLabel()
        self.movie_screen.setAlignment(Qt.AlignCenter)
        vbox = QVBoxLayout()
        vbox.addWidget(self.movie_screen)
        self.setLayout(vbox)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()
        self.movie.loopCount()

        groupbox.setLayout(vbox)

        return groupbox

    def createSecondExclusiveGroup(self):
        groupbox = QGroupBox('분류 결과/분류 성공률')

        btn1 = QPushButton('얼굴_썸네일', self)
        btn2 = QPushButton('다른사람', self)
        hbox1 = QHBoxLayout()

        btn3 = QLabel('사람수', self)
        btn4 = QLabel('사람수' + str(cnt) + "명", self)
        hbox2 = QHBoxLayout()

        hbox1.addWidget(btn1)
        hbox1.addWidget(btn2)
        hbox2.addWidget(btn3)
        hbox2.addWidget(btn4)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        groupbox.setLayout(vbox)

        return groupbox

    def createNonExclusiveGroup(self):
        groupbox = QGroupBox('진행되고있는 이미지')

        pixmap = QPixmap('target.jpg')
        # 스케일 조절 ㄱㄱ
        pixmap.scaled(120, 125)
        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_img)
        self.setLayout(vbox)
        groupbox.setLayout(vbox)

        return groupbox

    def webcam(self):
        global running
        label = QLabel()
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        label.resize(width, height)
        while running:
            ret, img = cap.read()
            if ret:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, c = img.shape
                qImg = QImage(img.data, w, h, w * c, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qImg)
                label.setPixmap(pixmap)
            else:
                QMessageBox.about(self, "Error", "Cannot read frame.")
                print("cannot read frame.")
                break

        cap.release()
        groupbox = QGroupBox('진행되고있는 이미지')
        vbox = QVBoxLayout()
        btn_start = QPushButton("Camera On")
        btn_stop = QPushButton("Camera Off")
        vbox.addWidget(label)
        vbox.addWidget(btn_start)
        vbox.addWidget(btn_stop)
        btn_start.clicked.connect(self.start)
        btn_stop.clicked.connect(self.stop)
        groupbox.setLayout(vbox)
        groupbox.show()
        return groupbox

    def stop(self):
        global running
        running = False
        print("stop")

    def start(self):
        global running
        running = True
        th = threading.Thread(target=self.webcam)
        th.start()
        print("start")

    def onExit(self):
        print("exit")
        self.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

