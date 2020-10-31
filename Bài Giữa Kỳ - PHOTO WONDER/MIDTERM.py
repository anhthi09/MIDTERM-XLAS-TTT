from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
import platform
import sys
import cv2
from math import *
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
import copy


## ==> GLOBALS
counter = 0

class SplashScreen(QtWidgets.QMainWindow):
    def __init__(self) -> QMainWindow:
        """

        :rtype: object
        """
        super(SplashScreen, self).__init__()
        uic.loadUi('splash_screen.ui', self)


        ## REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


        ## DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.dropShadowFrame.setGraphicsEffect(self.shadow)

        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(35)

        # CHANGE DESCRIPTION

        # Initial Text
        self.label_description.setText("<strong>WELCOME</strong> TO PHOTOWONDER")

        # Change Texts
        QtCore.QTimer.singleShot(1500, lambda: self.label_description.setText("<strong>LOADING</strong> "))
        QtCore.QTimer.singleShot(3000, lambda: self.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))

        self.show()

    def progress(self):
        global counter

        # SET VALUE TO PROGRESS BAR
        self.progressBar.setValue(counter)

        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            self.main = Ui_MainWindow()
            self.main.show()

            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        counter += 1



class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self)-> QMainWindow:
        super(Ui_MainWindow, self).__init__()
        uic.loadUi('MIDTERM.ui', self)
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
        self.btnMEAN_C.clicked.connect(self.MEAN_C)
        self.btnGAUSSIAN_C.clicked.connect(self.GAUSSIAN_C)
        self.btnBINARY.clicked.connect(self.BINARY)
        self.btnTOZERO.clicked.connect(self.TOZERO)
        self.btnTRUNC.clicked.connect(self.TRUNC)
        self.btnOTSU.clicked.connect(self.OTSU)
        self.btnSUBTRACT.clicked.connect(self.SUBTRACT)
        self.btnMULTIPLY.clicked.connect(self.MULTIPLY)
        self.btnGRAMMA.clicked.connect(self.GRAMMA)
        self.btnLinear.clicked.connect(self.Linear)
        self.btnSharpen.clicked.connect(self.Sharpen)
        self.btnBilateral.clicked.connect(self.Bilateral)
        self.btnSobel.clicked.connect(self.Sobel)
        self.btnPrewitt.clicked.connect(self.Prewitt)
        self.btnLaplacian.clicked.connect(self.Laplacian)
        self.btnDrectional.clicked.connect(self.Drectional)
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

    def MEAN_C(self):
        self.labelAfter.setText('AFTER APPLY MEAN_C FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        img = cv2.medianBlur(img, 5)
        th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                    cv2.THRESH_BINARY, 11, 2)

        images = th2
        self.ShowImageGray(images, self.iframe_new)

    def BINARY(self):
        self.labelAfter.setText('AFTER APPLY BINARY FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        img = cv2.medianBlur(img, 5)
        ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        images = th1
        self.ShowImageGray(images, self.iframe_new)

    def TOZERO(self):
        self.labelAfter.setText('AFTER APPLY TOZERO FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        img = cv2.medianBlur(img, 5)
        ret, thresh4 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)

        images = thresh4
        self.ShowImageGray(images, self.iframe_new)

    def TRUNC(self):
        self.labelAfter.setText('AFTER APPLY  TRUNC FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        img = cv2.medianBlur(img, 5)
        ret, thresh5 = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)

        images = thresh5
        self.ShowImageGray(images, self.iframe_new)

    def OTSU(self):
        self.labelAfter.setText('AFTER APPLY OTSU FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        img = cv2.medianBlur(img, 5)
        ret, thresh6 = cv2.threshold(img, 127, 255, cv2.THRESH_OTSU)

        images = thresh6
        self.ShowImageGray(images, self.iframe_new)


    def GAUSSIAN_C(self):
        self.labelAfter.setText('AFTER APPLY GAUSSIAN_C FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        img = cv2.medianBlur(img, 5)
        th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                    cv2.THRESH_BINARY, 11, 2)

        images = th3
        self.ShowImageGray(images, self.iframe_new)

    def SUBTRACT(self):
        self.labelAfter.setText('AFTER APPLY SUBTRACT FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        sub = cv2.subtract(img, self.szFilter)
        self.ShowImageGray(sub, self.iframe_new)
    def MULTIPLY(self):
        self.labelAfter.setText('AFTER APPLY MULTIPLY FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        sub = cv2.multiply(img, self.szFilter)
        self.ShowImageGray(sub, self.iframe_new)
    def GRAMMA(self):
        self.labelAfter.setText('AFTER APPLY GRAMMA FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        gra = np.power(img, self.szFilter)
        self.ShowImageGray(gra, self.iframe_new)
    def Linear(self):
        self.labelAfter.setText('AFTER APPLY Linear FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)

        def pixelVal(pix, r1, s1, r2, s2):
            if (0 <= pix and pix <= r1):
                return (s1 / r1) * pix
            elif (r1 < pix and pix <= r2):
                return ((s2 - s1) / (r2 - r1)) * (pix - r1) + s1
            else:
                return ((255 - s2) / (255 - r2)) * (pix - r2) + s2

        r1 = 70
        s1 = 0
        r2 = 140
        s2 = 255
        # Vectorize the function to apply it to each value in the Numpy array.
        pixelVal_vec = np.vectorize(pixelVal)

        # Apply contrast stretching.
        contrast_stretched = pixelVal_vec(img, r1, s1, r2, s2)

        self.ShowImageGray(contrast_stretched, self.iframe_new)

    def Sharpen(self):
        self.labelAfter.setText('AFTER APPLY SHARPEN FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpen_img = cv2.filter2D(img, self.szFilter, filter)

        self.ShowImageGray(sharpen_img, self.iframe_new)

    def Bilateral(self):
        self.labelAfter.setText('AFTER APPLY BILATERAL FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        blur2 = cv2.bilateralFilter(img,9,75,75)
        self.ShowImageGray(blur2, self.iframe_new)

    def Sobel(self):
        self.labelAfter.setText('AFTER APPLY SOBEL FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        kernel_Sobel_x = np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]])

        sobel = cv2.filter2D(img, -1, kernel_Sobel_x)
        self.ShowImageGray(sobel, self.iframe_new)

    def Prewitt(self):
        self.labelAfter.setText('AFTER APPLY PREWITT FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        kernel_Prewitt_x = np.array([
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1]])

        prewitt = cv2.filter2D(img, -1, kernel_Prewitt_x)
        self.ShowImageGray(prewitt, self.iframe_new)

    def Laplacian(self):
        self.labelAfter.setText('AFTER APPLY PREWITT FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        kernel_Laplacian_1 = np.array([
            [0, 1, 0],
            [1, -4, 1],
            [0, 1, 0]])

        laplacian = cv2.filter2D(img, -1, kernel_Laplacian_1)
        self.ShowImageGray(laplacian, self.iframe_new)

    def Drectional(self):
        self.labelAfter.setText('AFTER APPLY DRECTIONAL FILTER')
        self.szFilter = self.boxFilter.value()
        img = copy.copy(self.Gray)
        filter = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])/3
        img1 = cv2.filter2D(img, self.szFilter,filter )
        self.ShowImageGray(img1, self.iframe_new)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    app.exec_()