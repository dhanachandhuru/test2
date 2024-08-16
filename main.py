from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
                          QRect, QSize, QUrl, Qt, QTimer)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                         QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
                         QRadialGradient,QImage)
import cv2
from PyQt5.QtWidgets import *
import sys
import os
from ui_form import Ui_MainWindow





# import zipfile


class MainWindow(QtWidgets.QMainWindow):


    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ui.textEdit.setText(self.URL)
        self.ui.startButton.clicked.connect(self.start_reading)
        self.ui.stoplButton.clicked.connect(self.stop_reading)
        self.ui.shutDownButton_2.clicked.connect(self.cmdshutdown)

        self.ui.timer = QTimer(self)
        self.ui.timer.timeout.connect(self.update_image)

        # Open the camera (adjust the camera index as needed)
        self.ui.cap = cv2.VideoCapture(1)
        self.ui.is_capturing = False


    def cmdshutdown(self):
        print("cancle")
        self.close()
        window.close()


    def start_reading(self):
        print("start")
        self.ui.is_capturing = True
        self.ui.timer.start(30)
        # opencv

    def update_image(self):
        print("start")

        # opencv
        net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(320, 320), scale=1 / 355)

        # load classz
        classes = []
        with open("dnn_model/classes.txt", "r") as file_object:
            for class_name in file_object.readlines():
                class_name = class_name.strip()
                classes.append(class_name)

        print("objects list")
        print(classes)

        # initialize camera
        cap = cv2.VideoCapture(0)

        while True:
            # get frames
            ret, frame = cap.read()

            # object Detection

            (class_ids, scores, bboxes) = model.detect(frame)
            for class_id, score, bbox in zip(class_ids, scores, bboxes):
                (x, y, w, h) = bbox

                class_name = classes[class_id]
                cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (200, 0, 50), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 0, 50), 3)
                
            print("class ids", class_ids)
            print("score", scores)
            print("bboxes", bboxes)
            cv2.imshow("Frame", frame)

            cv2.waitKey(0)


    def stop_reading(self):
        print("stop")


    def tare_weight(self):
        print("tare")

    def displayImage(self, img, window=1):
        qformat = QImage.Format_Indexed8

        if len(img.shap) == 3:
            if(img.shape[2]) == 4:
                qformat = QImage.Format_RGBA888

            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()  # Maximized()

    sys.exit(app.exec_())
    print("exiting")
