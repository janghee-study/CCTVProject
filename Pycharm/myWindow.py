import sys
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import cv2
import threading
import time
from PyQt5.QtCore import QDateTime
import os

#py designer에서 ui긁어옴
form_class = uic.loadUiType("pixmapTest.ui")[0]
cnt = 0
file_count = 0
class WindowClass(QMainWindow, form_class):

    def __init__(self):
        global file_count
        file_count = sum(len(files) for _, _, files in os.walk(r'C:/Users/rlawk/PycharmProjects/pythonProject/thumbnail'))

        super().__init__()
        self.setupUi(self)
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load("CCTV2.jpg")
        self.CCTV.setPixmap(self.qPixmapFileVar)
        
        # 캡처한 사진
        self.qPixmapFileVar.load("target.jpg")
        self.label.setPixmap(self.qPixmapFileVar)

        self.date = QDate.currentDate()
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))
        self.show()

        # 버튼에 기능을 연결하는 코드
        self.start.clicked.connect(self.button1)
        self.first.clicked.connect(self.changeTextFunction)
        self.mid.clicked.connect(self.Up)

        # 바탕화면
        olmage = QImage("paint.jpg")
        slmage = olmage.scaled(QSize(1000,1000))
        palette = QPalette()
        palette.setBrush(10,QBrush(slmage))
        self.setPalette(palette)

    def changeTextFunction(self):
        self.btn_changeText.setText(str(file_count))

    # button이 눌리면 작동할 함수
    def button1(self):
        self.qPixmapFileVar.load("thumbnail/thumbnail"+str(cnt)+".png")
        self.face.setPixmap(self.qPixmapFileVar)

    # 썸네일 숫자 카운트함수
    def Up(self):
        global cnt
        cnt+=1
        if(cnt==file_count):
            cnt=0

running = False
def run(self):
    global running
    cap = cv2.VideoCapture(0)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    self.label.resize(width, height)
    while running:
        ret, img = cap.read()
        if ret:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h,w,c = img.shape
            qImg = self.QImage(img.data, w, h, w*c, self.QImage.Format_RGB888)
            pixmap = self.QPixmap.fromImage(qImg)
            self.label.setPixmap(pixmap)
        else:
            # QtWidgets.QMessageBox.about(win, "Error", "Cannot read frame.")
            print("cannot read frame.")
            break
    cap.release()
    print("Thread end.")

def stop():
    global running
    running = False
    print("stoped..")

def start():
    global running
    running = True
    th = threading.Thread(target=run)
    th.start()
    print("started..")

if __name__ == "__main__" :

    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()