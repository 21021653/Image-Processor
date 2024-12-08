from PIL import Image
import subprocess
import os
import cv2
from PIL import Image, ImageEnhance, ImageQt
from super_resolution import super_resolve
from brightness_sharpness import adjust_sharpness, adjust_brightness
from filter import apply_filter
from color import adjust_hue, adjust_saturation, adjust_temperature 
import numpy as np

from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QLineEdit,QWidget, QTabWidget, QSlider, QComboBox
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import sys
import PyQt6

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("convert.ui", self)
        self.setWindowTitle("Image Enhancer")
        self.tabwidget = self.findChild(QTabWidget, "tabWidget")

        self.tab = self.findChild(QWidget, "tab")
        self.label = self.findChild(QLabel, "label")

        self.button = self.findChild(QPushButton, "pushButton")
        self.button.clicked.connect(self.super_resolution)

        self.label2 = self.findChild(QLabel, "label_2")
        self.button2 = self.findChild(QPushButton, "pushButton_2")
        self.button2.clicked.connect(self.clicker2)

        self.button3 = self.findChild(QPushButton, "pushButton_3")
        self.button3.clicked.connect(self.clicker3)

        self.label19 = self.findChild(QLabel, "label_19")
        self.label20 = self.findChild(QLabel, "label_20")
        

        self.modelBox = self.findChild(QComboBox,"comboBox_2")
        self.modelBox.addItem("EDSR")
        self.modelBox.addItem("ESPCN")
        self.modelBox.addItem("FSRCNN")
        self.modelBox.addItem("LAPSRN")
        global model_name
        model_name = self.modelBox.currentText()


        ##############################################################################
        self.tab2 = self.findChild(QWidget, "tab_2")
        self.label5 = self.findChild(QLabel, "label_5")
        self.button5 = self.findChild(QPushButton, "pushButton_5")
        self.button5.clicked.connect(self.clicker5)

        self.button4 = self.findChild(QPushButton, "pushButton_4")
        self.button4.clicked.connect(self.clicker4)
        self.label4 = self.findChild(QLabel, "label_4")

        self.sharp_slider = self.findChild(QSlider,"horizontalSlider_2")
        self.sharp_slider.valueChanged.connect(self.sharpness_slided)

        self.bright_slider = self.findChild(QSlider,"horizontalSlider_3")
        self.bright_slider.valueChanged.connect(self.brightness_slided)

        self.hue_slider = self.findChild(QSlider,"horizontalSlider_4")
        self.hue_slider.valueChanged.connect(self.hue_slided)

        self.saturation_slider = self.findChild(QSlider,"horizontalSlider_5")
        self.saturation_slider.valueChanged.connect(self.saturation_slided)

        self.temp_slider = self.findChild(QSlider,"horizontalSlider_6")
        self.temp_slider.valueChanged.connect(self.temp_slided)


        self.label13 = self.findChild(QLabel, "label_13")
        self.label14 = self.findChild(QLabel, "label_14")
        self.label15 = self.findChild(QLabel, "label_15")
        self.label16 = self.findChild(QLabel, "label_16")
        self.label17 = self.findChild(QLabel, "label_17")
        self.label18 = self.findChild(QLabel, "label_18")
        self.label21 = self.findChild(QLabel, "label_21")
        self.label22 = self.findChild(QLabel, "label_22")
        self.label23 = self.findChild(QLabel, "label_23")
        self.label24 = self.findChild(QLabel, "label_24")
        self.label25 = self.findChild(QLabel, "label_25")
        self.label26 = self.findChild(QLabel, "label_26")

        ###############################################################################
        self.tab3 = self.findChild(QWidget, "tab_3")
        self.button7 = self.findChild(QPushButton, "pushButton_7")
        self.button7.clicked.connect(self.clicker7)

        self.button9 = self.findChild(QPushButton, "pushButton_9")
        self.button9.clicked.connect(self.clicker9)

        self.comboBox = self.findChild(QComboBox,"comboBox")
        self.comboBox.addItem("Median Filter")
        self.comboBox.addItem("Gaussian Filter")
        self.comboBox.addItem("Box Filter")
        self.comboBox.addItem("NL Means")
        global filter_type
        filter_type = self.comboBox.currentText()

        self.label7 = self.findChild(QLabel, "label_7")
        self.label8 = self.findChild(QLabel, "label_8")
        self.label9 = self.findChild(QLabel, "label_9")
        self.label10 = self.findChild(QLabel, "label_10")
        self.label11 = self.findChild(QLabel, "label_11")
        self.label12 = self.findChild(QLabel, "label_12")

        self.slider = self.findChild(QSlider, "horizontalSlider")
        self.slider.setMinimum(3)
        self.slider.setMaximum(15)
        self.slider.setTickInterval(2)
        self.slider.valueChanged.connect(self.filter_slided)
        self.show()


    def clicker2(self):
        fname = QFileDialog.getSaveFileName(self, "Set File Name", "D://OFVS//videos","JPG Files (*.jpg);;PNG Files(*.png)" )
        if fname2 and fname:
            out_rgb = cv2.cvtColor(resol_out, cv2.COLOR_BGR2RGB)
            out_pil = Image.fromarray(out_rgb)
            out_pil.save(fname[0])

    def clicker3(self):
        global fname2
        fname2 = QFileDialog.getOpenFileName(self, "Open File", "D://OFVS//videos","JPG Files (*.jpg *.jpeg);;PNG Files(*.png)")
        self.pixmap5 = QPixmap(fname2[0])
        self.label19.setPixmap(self.pixmap5.scaled(self.label19.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
    def super_resolution(self):
        if fname2:
            global resol_out
            resol_out = super_resolve(fname2[0],model_name)
            height, width, channel = resol_out.shape
            bytes_per_line = channel * width
            q_image = QImage(resol_out.data,width, height, bytes_per_line, QImage.Format.Format_BGR888)
            self.pixmap6 = QPixmap.fromImage(q_image)
            self.label20.setPixmap(self.pixmap6.scaled(self.label20.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    ##################################################################################################
    def clicker5(self):
        global fname3
        fname3 = QFileDialog.getOpenFileName(self, "Open File", "D://OFVS//videos","JPG Files (*.jpg);;PNG Files(*.png)")
        self.pixmap3 = QPixmap(fname3[0])
        self.label15.setPixmap(self.pixmap3.scaled(self.label15.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def clicker4(self):
        fname4 = QFileDialog.getSaveFileName(self, "Set File Name", "D://OFVS//videos","JPG Files (*.jpg);;PNG Files(*.png)" )
        if fname4 and fname3:
            if sharp_out is not None:
                out_rgb = cv2.cvtColor(sharp_out, cv2.COLOR_BGR2RGB)
            elif bright_out is not None:
                out_rgb = cv2.cvtColor(bright_out, cv2.COLOR_BGR2RGB)
            elif hue_out is not None:
                out_rgb = cv2.cvtColor(hue_out, cv2.COLOR_BGR2RGB)
            elif saturation_out is not None:
                out_rgb = cv2.cvtColor(saturation_out, cv2.COLOR_BGR2RGB)
            elif temperature_out is not None:
                out_rgb = cv2.cvtColor(temperature_out, cv2.COLOR_BGR2RGB)    
            out_pil = Image.fromarray(out_rgb)
            out_pil.save(fname4[0])

    def sharpness_slided(self,value):
        global sharp_out
        sharp_out =  adjust_sharpness(fname3[0],value)
        q_image = ImageQt.ImageQt(sharp_out)
        sharp_out = np.array(sharp_out)
        self.pixmap4 = QPixmap.fromImage(q_image)
        self.label16.setPixmap(self.pixmap4.scaled(self.label16.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.sharp_slider.setValue(value)
        self.label17.setText(str(value))

    def brightness_slided(self,value):
        global bright_out
        bright_out = adjust_brightness(fname3[0], value)
        height, width, channel = bright_out.shape
        bright_out = np.array(bright_out)
        bytes_per_line = channel * width
        q_image = QImage(bright_out.data,width, height, bytes_per_line, QImage.Format.Format_BGR888)
        self.pixmap4 = QPixmap.fromImage(q_image)
        self.label16.setPixmap(self.pixmap4.scaled(self.label16.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.bright_slider.setValue(value)
        self.label18.setText(str(value))

    def hue_slided(self,value):
        global hue_out
        hue_out = adjust_hue(fname3[0], value)
        hue_out = np.array(hue_out)
        height, width, channel = hue_out.shape
        bytes_per_line = channel * width
        q_image = QImage(hue_out.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
        self.pixmap4 = QPixmap.fromImage(q_image)
        self.label16.setPixmap(self.pixmap4.scaled(self.label16.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.hue_slider.setValue(value)
        self.label22.setText(str(value))

    def saturation_slided(self,value):
        global saturation_out
        saturation_out = adjust_saturation(fname3[0], value)
        saturation_out = np.array(saturation_out)
        height, width, channel = saturation_out.shape
        bytes_per_line = channel * width
        q_image = QImage(saturation_out.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
        self.pixmap4 = QPixmap.fromImage(q_image)
        self.label16.setPixmap(self.pixmap4.scaled(self.label16.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.saturation_slider.setValue(value)
        self.label24.setText(str(value))

    def temp_slided(self,value):
        global temperature_out
        temperature_out = adjust_saturation(fname3[0], value)
        temperature_out = np.array(temperature_out)
        height, width, channel = temperature_out.shape
        bytes_per_line = channel * width
        q_image = QImage(temperature_out.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
        self.pixmap4 = QPixmap.fromImage(q_image)
        self.label16.setPixmap(self.pixmap4.scaled(self.label16.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.temp_slider.setValue(value)
        self.label26.setText(str(value))

    ##################################################################################################
    def clicker7(self):
        global fname6
        fname6 = QFileDialog.getOpenFileName(self, "Open File", "D://OFVS//videos","JPG Files (*.jpg);;PNG Files(*.png)")
        self.pixmap1 = QPixmap(fname6[0])
        self.label7.setPixmap(self.pixmap1.scaled(self.label7.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def filter_slided(self,value):
        if value % 2 == 0:
            value = value - 1 if value > self.slider.value() else value + 1
        self.slider.setValue(value)
        if fname6:
            global filter_out
            filter_out = apply_filter(fname6[0],filter_type,value)
            height, width, channel = filter_out.shape
            bytes_per_line = channel * width
            q_image = QImage(filter_out.data,width, height, bytes_per_line, QImage.Format.Format_BGR888)
            self.pixmap2 = QPixmap.fromImage(q_image)
            self.label8.setPixmap(self.pixmap2.scaled(self.label8.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.label12.setText(str(value))

    def clicker9(self):
        fname7 = QFileDialog.getSaveFileName(self, "Set File Name", "D://OFVS//videos","JPG Files (*.jpg);;PNG Files(*.png)" )
        if fname7 and fname6:
            out_rgb = cv2.cvtColor(filter_out, cv2.COLOR_BGR2RGB)
            out_pil = Image.fromarray(out_rgb)
            out_pil.save(fname6[0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec()
