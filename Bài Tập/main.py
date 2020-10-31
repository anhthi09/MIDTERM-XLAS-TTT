from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import sys
import cv2
from math import *
from matplotlib import pyplot as plt
import numpy as np
import copy


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        uic.loadUi('Conv2D.ui', self)
        self.origin = None
        self.Gray = None
        self.szFilter = None
        self.actionOpen.triggered.connect(self.openFile)
        self.actionExit.triggered.connect(self.Exit)
        self.btnMean.clicked.connect(self.Mean)
        self.btnBlur.clicked.connect(self.Blur)
        self.btnGauss.clicked.connect(self.Gauss)
        self.btnMedian.clicked.connect(self.Median)
        self.btnGx.clicked.connect(self.Gx)
        self.btnGy.clicked.connect(self.Gy)
        self.btnGxAddGy.clicked.connect(self.GxAddGy)
        self.btnGxDivGy.clicked.connect(self.GxDivGy)
        self.Segmentation.clicked.connect(self.Thresholding)
        self.THRESH_GAUSSIAN_C.clicked.connect(self.Threshold)
        self.BINARY.clicked.connect(self.Thresholding1)
        self.TOZERO.clicked.connect(self.Thresholding2)
        self.TRUNC.clicked.connect(self.Thresholding3)
        self.OTSU.clicked.connect(self.Thresholding4)

        self.show()

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*.png *.xpm *.jpg *.jpeg *.tif);;Python Files (*.py)",
                                                  options=options)

        self.image = cv2.imread(fileName)

        if (self.image.shape[1] > self.iframe_old.width() or self.image.shape[0] > self.iframe_old.height()):
            self.image = cv2.resize(self.image, (self.iframe_old.width(), self.iframe_old.height()))
        self.origin = self.image
        self.Gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.ShowImageGray(self.Gray, self.iframe_old)

    def Exit(self):
        quit(0)

    def ShowImageGray(self, image, label):
        label.clear()
        image = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                             QtGui.QImage.Format_Grayscale8).rgbSwapped()

        label.setPixmap(QtGui.QPixmap.fromImage(image))

    def getGx(self):
        img = copy.copy(self.Gray)
        filterGx = np.array([
            [0,0,0],
            [-1,2,-1],
            [0,0,0]
        ])
        img_Gx = cv2.filter2D(img, -1, filterGx)
        return img_Gx
        #test = img_Gx + self.getGy()
        #self.ShowImageGray(img_Gx, self.iframe_new)

    def getGy(self):
        img = copy.copy(self.Gray)
        filterGy = np.array([
            [0,-1,0],
            [0,2,0],
            [0,-1,0]
        ])
        img_Gy = cv2.filter2D(img, -1, filterGy)
        return img_Gy

    def Gx(self):
        self.labelAfter.setText('AFTER GX')
        self.ShowImageGray(self.Gray-self.getGx(), self.iframe_new)

    def Gy(self):
        self.labelAfter.setText('AFTER GY')
        self.ShowImageGray(self.getGy(), self.iframe_new)

    def GxAddGy(self):
        self.labelAfter.setText('AFTER Gx + Gy')
        img = self.getGx() + self.getGy()
        self.ShowImageGray(img, self.iframe_new)

    def GxDivGy(self):
        self.labelAfter.setText('AFTER Gx/Gy')
        imgGx = self.getGx()
        imgGy = self.getGy()
        print(imgGx)
        print(imgGy)
        res = copy.copy(imgGx)
        for i in range(len(imgGx)):
            for j in range(len(imgGx[i])):
                if (imgGy[i][j] == 0):
                    continue
                res[i][j] = imgGx[i][j]/imgGy[i][j]*2
                #res[i][j]=atan(res[i][j])
        res = np.uint8(res)
        print(res)
        self.ShowImageGray(res, self.iframe_new)

    def Mean(self):
        self.labelAfter.setText('AFTER APPLY MEAN FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        img_filter = np.ones(shape=(self.szFilter, self.szFilter))
        img_filter = img_filter / sum(img_filter)
        img_mean = cv2.filter2D(img, -1, img_filter)
        self.ShowImageGray(img_mean, self.iframe_new)

    def Blur(self):
        self.labelAfter.setText('AFTER APPLY BLUR FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        blur = cv2.blur(img, (self.szFilter, self.szFilter))
        self.ShowImageGray(blur, self.iframe_new)


    def Gauss(self):
        self.labelAfter.setText('AFTER APPLY GAUSS FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        gauss = cv2.GaussianBlur(img, (self.szFilter, self.szFilter),0)
        self.ShowImageGray(gauss, self.iframe_new)


    def Median(self):
        self.labelAfter.setText('AFTER APPLY MEDIAN FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        median = cv2.medianBlur(img, self.szFilter)
        self.ShowImageGray(median, self.iframe_new)

    def Thresholding(self):

        img = copy.copy(self.Gray)
        img = cv2.medianBlur(img, 5)
        th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                    cv2.THRESH_BINARY, 11, 2)

        images = th2
        self.ShowImageGray(images, self.iframe_new)

    def Thresholding1(self):

        img = copy.copy(self.Gray)
        img = cv2.medianBlur(img, 5)
        ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        images = th1
        self.ShowImageGray(images, self.iframe_new)

    def Thresholding2(self):

        img = copy.copy(self.Gray)
        img = cv2.medianBlur(img, 5)
        ret, thresh4 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)

        images = thresh4
        self.ShowImageGray(images, self.iframe_new)

    def Thresholding3(self):

        img = copy.copy(self.Gray)
        img = cv2.medianBlur(img, 5)
        ret, thresh5 = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)

        images = thresh5
        self.ShowImageGray(images, self.iframe_new)

    def Thresholding4(self):

        img = copy.copy(self.Gray)
        img = cv2.medianBlur(img, 5)
        ret, thresh6 = cv2.threshold(img, 127, 255, cv2.THRESH_OTSU)

        images = thresh6
        self.ShowImageGray(images, self.iframe_new)


    def Threshold(self):

        img = copy.copy(self.Gray)
        img = cv2.medianBlur(img, 5)
        th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                    cv2.THRESH_BINARY, 11, 2)

        images = th3
        self.ShowImageGray(images, self.iframe_new)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MainWindow()
    app.exec_()
