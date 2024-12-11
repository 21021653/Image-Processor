from PIL import Image
import cv2
from PIL import Image, ImageQt
from super_resolution import super_resolve
from filter import apply_filter, psnr, plot_images, add_noise
from color import adjust_hue, adjust_saturation, adjust_temperature, adjust_sharpness, adjust_brightness 
from histogram import histogram_equalization_color
import time
import numpy as np

from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QWidget, QTabWidget, QSlider, QComboBox
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import sys
import PyQt6

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("main.ui", self)
        self.setWindowTitle("Image Enhancer")
        self.tabwidget = self.findChild(QTabWidget, "tabWidget")

        self.tab = self.findChild(QWidget, "tab")
        
        self.button = self.findChild(QPushButton, "pushButton")
        self.button.clicked.connect(self.super_resolution)

        self.button2 = self.findChild(QPushButton, "pushButton_2")
        self.button2.clicked.connect(self.clicker2)

        self.button3 = self.findChild(QPushButton, "pushButton_3")
        self.button3.clicked.connect(self.clicker3)

        self.label = self.findChild(QLabel, "label")
        self.label2 = self.findChild(QLabel, "label_2")
        self.label19 = self.findChild(QLabel, "label_19")
        self.label20 = self.findChild(QLabel, "label_20")
        self.label66 = self.findChild(QLabel, "label_66")
        self.label67 = self.findChild(QLabel, "label_67")
        self.label68 = self.findChild(QLabel, "label_68")
        self.label69 = self.findChild(QLabel, "label_69")
        self.label70 = self.findChild(QLabel, "label_70")

        self.modelBox = self.findChild(QComboBox,"comboBox_2")
        self.modelBox.addItems(["(none)","EDSR_x3","EDSR_x4","ESPCN_x3","ESPCN_x4","FSRCNN_x4","LAPSRN_x4", "Bicubic_x3", "Bicubic_x4", "Lanczos_x3", "Lanczos_x4"])
        
        
        ##############################################################################
        self.tab2 = self.findChild(QWidget, "tab_2")
        
        self.button5 = self.findChild(QPushButton, "pushButton_5")
        self.button5.clicked.connect(self.clicker5)

        self.button4 = self.findChild(QPushButton, "pushButton_4")
        self.button4.clicked.connect(self.clicker4)
        
        self.sharp_slider = self.findChild(QSlider,"horizontalSlider_2")
        self.sharp_slider.setRange(-50, 50)  # -50 = darker, 0 = original, 50 = brighter
        self.sharp_slider.setValue(0)
        self.sharp_slider.valueChanged.connect(self.update_image)

        self.bright_slider = self.findChild(QSlider,"horizontalSlider_3")
        self.bright_slider.setRange(-50, 50)  # -50 = darker, 0 = original, 50 = brighter
        self.bright_slider.setValue(0)
        self.bright_slider.valueChanged.connect(self.update_image)

        self.hue_slider = self.findChild(QSlider,"horizontalSlider_4")
        self.hue_slider.setRange(-50, 50)  # -50 = darker, 0 = original, 50 = brighter
        self.hue_slider.setValue(0)
        self.hue_slider.valueChanged.connect(self.update_image)

        self.saturation_slider = self.findChild(QSlider,"horizontalSlider_5")
        self.saturation_slider.setRange(-50, 50)  # -50 = darker, 0 = original, 50 = brighter
        self.saturation_slider.setValue(0)
        self.saturation_slider.valueChanged.connect(self.update_image)

        self.temp_slider = self.findChild(QSlider,"horizontalSlider_6")
        self.temp_slider.setRange(-50, 50)  # -50 = darker, 0 = original, 50 = brighter
        self.temp_slider.setValue(0)
        self.temp_slider.valueChanged.connect(self.update_image)

        self.label4 = self.findChild(QLabel, "label_4")
        self.label5 = self.findChild(QLabel, "label_5")
        self.label13 = self.findChild(QLabel, "label_13")
        self.label14 = self.findChild(QLabel, "label_14")
        self.label15 = self.findChild(QLabel, "label_15")
        self.label16 = self.findChild(QLabel, "label_16")
        self.label21 = self.findChild(QLabel, "label_21")
        self.label23 = self.findChild(QLabel, "label_23")
        self.label25 = self.findChild(QLabel, "label_25")

        ###############################################################################
        self.tab3 = self.findChild(QWidget, "tab_3")
        self.button7 = self.findChild(QPushButton, "pushButton_7")
        self.button7.clicked.connect(self.clicker7)

        self.button23 = self.findChild(QPushButton, "pushButton_23")
        self.button23.clicked.connect(self.clicker23)

        self.button24 = self.findChild(QPushButton, "pushButton_24")
        self.button24.clicked.connect(self.clicker24)

        self.button25 = self.findChild(QPushButton, "pushButton_25")
        self.button25.clicked.connect(self.filtered)

        self.comboBox = self.findChild(QComboBox,"comboBox")
        self.comboBox.addItems(["(none)","Salt and Pepper", "Gaussian", "Poisson"])

        self.comboBox3 = self.findChild(QComboBox,"comboBox_3")
        self.comboBox3.addItems(["(none)","Median Filter","Gaussian Filter","Box Filter","Butterworth Filter","NL Means"])

        self.comboBox4 = self.findChild(QComboBox,"comboBox_4")
        self.comboBox4.addItems(["3","5","7","9","11","13","15"])


        self.label3 = self.findChild(QLabel, "label_3")
        self.label43 = self.findChild(QLabel, "label_43")
        self.label6 = self.findChild(QLabel, "label_6")
        self.label7 = self.findChild(QLabel, "label_7")
        self.label8 = self.findChild(QLabel, "label_8")

        #############################################################################
        self.tab4 = self.findChild(QWidget, "tab_4")
        self.button6 = self.findChild(QPushButton, "pushButton_6")
        self.button6.clicked.connect(self.clicker6)

        self.button8 = self.findChild(QPushButton, "pushButton_8")
        self.button8.clicked.connect(self.equalize_histogram)

        self.button10 = self.findChild(QPushButton, "pushButton_10")
        self.button10.clicked.connect(self.clicker10)

        self.label27 = self.findChild(QLabel, "label_27")
        self.label28 = self.findChild(QLabel, "label_28")
        self.label29 = self.findChild(QLabel, "label_29")
        self.label30 = self.findChild(QLabel, "label_30")

        self.show()

    def clicker2(self):
        fname = QFileDialog.getSaveFileName(self, "Set File Name","","JPG Files (*.jpg *.jpeg);;PNG Files(*.png)" )
        if fname2[0] is not None and fname[0] is not None and resol_out is not None:
            out_rgb = cv2.cvtColor(resol_out, cv2.COLOR_BGR2RGB)
            out_pil = Image.fromarray(out_rgb)
            out_pil.save(fname[0])

    def clicker3(self):
        global fname2
        fname2 = QFileDialog.getOpenFileName(self, "Open File","","JPG Files (*.jpg *.jpeg);;PNG Files(*.png)")
        if fname2[0] is not None:
            self.pixmap5 = QPixmap(fname2[0])
            self.label19.setPixmap(self.pixmap5.scaled(self.label19.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
    def super_resolution(self):
        if fname2[0] is not None:
            inp = cv2.imread(fname2[0])
            original_height, original_width, _ = inp.shape
            global resol_out
            model_name = self.modelBox.currentText()
            if model_name != "(none)":
                start = time.time()
                resol_out = super_resolve(fname2[0],model_name)
                end = time.time()
                elapsed_time = end - start
                height, width, _ = resol_out.shape
                psnr_value,_ = psnr(inp,resol_out)
                self.display_image(resol_out,self.label20)
                self.label68.setText(f"{original_width}x{original_height}")
                self.label70.setText(f"{width}x{height}")
                self.label66.setText(f"PSNR: {psnr_value:.2f}")
                print(f"Running time : {elapsed_time}")


    ##################################################################################################
    def clicker5(self):
        global fname3
        global inp_original
        
        fname3 = QFileDialog.getOpenFileName(self, "Open File","","JPG Files (*.jpg *.jpeg);;PNG Files(*.png)")
        if fname3[0] is not None:
            inp_original = Image.open(fname3[0])
            self.pixmap3 = QPixmap(fname3[0])
            self.label15.setPixmap(self.pixmap3.scaled(self.label15.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.label16.setPixmap(self.pixmap3.scaled(self.label16.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def clicker4(self):
        if inp_current is not None:
            fname4 = QFileDialog.getSaveFileName(self, "Set File Name","","JPG Files (*.jpg *.jpeg);;PNG Files(*.png)" )
            if fname4[0] is not None:
                inp_current.save(fname4[0])

    def update_image(self):
        # Hàm điều chỉnh cả sharpness, brightness và màu sắc
        global inp_current
        if not 'inp_original' in globals() or inp_original is None:
            print("Error. Please load an image before adjusting sliders.")
            return
        if inp_original is not None:
            # Lấy giá trị thanh trượt
            self.hue_value = self.hue_slider.value()
            self.saturation_value = self.saturation_slider.value() 
            self.temperature_value = self.temp_slider.value()
            self.brightness_value = self.bright_slider.value()
            self.sharpness_value = self.sharp_slider.value()

            img = inp_original.copy()
            img = adjust_hue(img, self.hue_value)
            img = adjust_saturation(img, self.saturation_value)
            img = adjust_temperature(img, self.temperature_value)
            img = adjust_brightness(img, self.brightness_value)
            img = adjust_sharpness(img, self.sharpness_value)

            # Cập nhật ảnh hiện tại và hiển thị
            inp_current = img
            self.display_image(img,self.label16)
            self.label13.setText(f"Sharpness: {self.sharpness_value}")
            self.label14.setText(f"Brightness: {self.brightness_value}")
            self.label21.setText(f"Hue: {self.hue_value}")
            self.label23.setText(f"Saturation: {self.saturation_value}")
            self.label25.setText(f"Temperature: {self.temperature_value}")

    ##################################################################################################
    def clicker7(self):
        global fname6
        fname6 = QFileDialog.getOpenFileName(self, "Open File","","JPG Files (*.jpg *.jpeg);;PNG Files(*.png)")
        if fname6[0] is not None:
            self.pixmap1 = QPixmap(fname6[0])
            self.label7.setPixmap(self.pixmap1.scaled(self.label7.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def filtered(self):
        #Áp dụng filter dựa trên lựa chọn
        global filter_out
        if fname6[0] is not None:
            filter_type = self.comboBox3.currentText()
            kernel_strength = self.comboBox4.currentText()
            if filter_type != "(none)":
                start = time.time()
                filter_out = apply_filter(fname6[0],filter_type,kernel_strength)
                end = time.time()
                elapsed_time = end - start
                self.display_image(filter_out,self.label7)
                print(f"Running time: {elapsed_time}s")
            
    def clicker24(self):
        if fname6[0] is not None:
            noise_type = self.comboBox.currentText()
            filter_type = self.comboBox3.currentText()
            kernel_strength = self.comboBox4.currentText()
            if filter_type != "(none)" and noise_type != "(none)":
                inp = cv2.imread(fname6[0])
                noise_out = add_noise(fname6[0],noise_type)
                start = time.time()
                filter_out = apply_filter(noise_out,filter_type,kernel_strength)
                end = time.time()
                elapsed_time = end - start
                print(f"Running time: {elapsed_time}s")
                _,mse_value = psnr(inp,filter_out)
                plot_images(inp, noise_out, filter_out, filter_type, mse_value)

    def clicker23(self):
        fname7 = QFileDialog.getSaveFileName(self, "Set File Name","","JPG Files (*.jpg *.jpeg);;PNG Files(*.png)" )
        if fname7[0] and filter_out is not None:
            out_rgb = cv2.cvtColor(filter_out, cv2.COLOR_BGR2RGB)
            out_pil = Image.fromarray(out_rgb)
            out_pil.save(fname7[0])
    

    #################################################################################################
    def clicker6(self):
        global fname8
        fname8 = QFileDialog.getOpenFileName(self, "Open File","","JPG Files (*.jpg *.jpeg);;PNG Files(*.png)")
        if fname8[0] is not None:
            self.pixmap0 = QPixmap(fname8[0])
            self.label27.setPixmap(self.pixmap0.scaled(self.label27.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def equalize_histogram(self):
        if fname8[0] is not None:
            global equalized_out
            equalized_out = histogram_equalization_color(fname8[0], display=True)
            self.display_image(equalized_out,self.label28)

    def clicker10(self):
        fname9 = QFileDialog.getSaveFileName(self, "Set File Name","","JPG Files (*.jpg *.jpeg);;PNG Files(*.png)" )
        if fname8[0] is not None and fname9[0] is not None:
            equalized_out.save(fname9[0])

    def display_image(self, image, label):
        if isinstance(image, Image.Image):
            image = image
        else:
            image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        img_out = ImageQt.ImageQt(image)
        self.pixmap = QPixmap.fromImage(img_out)
        label.setPixmap(self.pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec()
