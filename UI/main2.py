import cv2
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QGridLayout

faceCascade = cv2.CascadeClassifier('./Cascade/haarcascade_frontalface_default.xml')

imgNum = 0
class ShowVideo(QtCore.QObject):

    flag = 0

    camera = cv2.VideoCapture(0)

    ret, image = camera.read()
    height, width = image.shape[:2]
    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)
    VideoSignal2 = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

    @QtCore.pyqtSlot()
    def startVideo(self):
        global image
        global faces
        run_video = True
        while run_video:
            ret, image = self.camera.read()
            ret1, image1 = self.camera.read()
            ret1, image2 = self.camera.read()

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #얼굴인식
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray)

            image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB) #얼굴출력


            qt_image1 = QtGui.QImage(image1.data,
                                     self.width,
                                     self.height,
                                     image1.strides[0],
                                     QtGui.QImage.Format_RGB888)
            self.VideoSignal1.emit(qt_image1)

            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x - 3, y - 3), (x + w + 3, y + h + 3), (0, 0, 255), 2)
            qt_image2 = QtGui.QImage(image.data,
                                     self.width,
                                     self.height,
                                     image.strides[0],
                                     QtGui.QImage.Format_RGB888)
            self.VideoSignal2.emit(qt_image2)

            if len(faces) > 1:
                print("두명이상 검출되었습니다.")
                return cv2.imwrite("C:/Users/rlawk/PycharmProjects/pythonProject/target.jpg", image2)

            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(25, loop.quit) #25 ms
            loop.exec_()

    def thumbnailCount(self):
        imgCnt = cv2.imread("C:/Users/rlawk/PycharmProjects/pythonProject/target.jpg")
        global imgNum
        for (x, y, w, h) in faces:
            cropped = imgCnt[y - int(h / 10):y + h + int(h / 10), x - int(w / 10):x + w + int(w / 10)]
            resize_img = cv2.resize(cropped, (350, 350))
            cv2.imwrite("C:/Users/rlawk/PycharmProjects/pythonProject/thumbnail/thumbnail" + str(imgNum) + ".png"
                        ,resize_img)
            imgNum += 1

    #썸네일 클릭만들기!
    def thumbnailPhoto(self):
        image = cv2.imread("C:/Users/rlawk/PycharmProjects/pythonProject/thumbnail/thumbnail" + str(imgNum) + ".png"
                           , cv2.IMREAD_ANYCOLOR)
        cv2.imshow("Thumbnail", image)




class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0,0, self.image)
        self.image = QtGui.QImage()

    def initUI(self):
        self.setWindowTitle('Test')


    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")
        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)


    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)

    image_viewer1 = ImageViewer()
    image_viewer2 = ImageViewer()

    vid.VideoSignal1.connect(image_viewer1.setImage)
    vid.VideoSignal2.connect(image_viewer2.setImage)

    push_button1 = QtWidgets.QPushButton('시작/정지')
    push_button1.clicked.connect(vid.startVideo)
    push_button2 = QtWidgets.QPushButton('썸네일')
    push_button2.clicked.connect(vid.thumbnailCount)
    push_button3 = QtWidgets.QPushButton('썸네일보기')
    push_button3.clicked.connect(vid.thumbnailPhoto)
    label = QtWidgets.QLabel("made by janghee")
    label.setAlignment(QtCore.Qt.AlignVCenter)

    vbox = QtWidgets.QVBoxLayout()
    hbox = QtWidgets.QHBoxLayout()
    hbox2 = QtWidgets.QHBoxLayout()
    hbox.addWidget(image_viewer1)
    hbox.addWidget(image_viewer2)
    hbox2.addWidget(push_button1)
    hbox2.addWidget(push_button2)
    hbox2.addWidget(push_button3)
    hbox2.addWidget(label)
    vbox.addLayout(hbox)
    vbox.addLayout(hbox2)

    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vbox)

    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.setWindowTitle("OpenCV영상처리")
    main_window.show()
    sys.exit(app.exec_())