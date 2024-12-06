from PIL import Image
import subprocess
import os
import cv2

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
        self.button.clicked.connect(self.clicker)

        
        self.label2 = self.findChild(QLabel, "label_2")
        self.button2 = self.findChild(QPushButton, "pushButton_2")
        self.button2.clicked.connect(self.clicker2)

        self.button3 = self.findChild(QPushButton, "pushButton_3")
        self.button3.clicked.connect(self.clicker3)

        self.entry = self.findChild(QLineEdit, "lineEdit")
        self.entry.setObjectName("input_field")

        self.entry2 = self.findChild(QLineEdit, "lineEdit_2")
        self.entry2.setObjectName("output_field")


        ###############################
        self.tab2 = self.findChild(QWidget, "tab_2")
        self.label5 = self.findChild(QLabel, "label_5")
        self.button5 = self.findChild(QPushButton, "pushButton_5")
        self.button5.clicked.connect(self.clicker5)

        self.label4 = self.findChild(QLabel, "label_4")


        self.bright_slider = self.findChild(QSlider,"horizontalSlider_3")
        self.bright_slider.valueChanged.connect(self.brightness_slided)

        self.label14 = self.findChild(QLabel, "label_14")
        self.label15 = self.findChild(QLabel, "label_15")
        self.label16 = self.findChild(QLabel, "label_16")
        self.label17 = self.findChild(QLabel, "label_17")
        self.label18 = self.findChild(QLabel, "label_18")

        ##############################
        self.tab3 = self.findChild(QWidget, "tab_3")
        self.button7 = self.findChild(QPushButton, "pushButton_7")
        self.button7.clicked.connect(self.clicker7)

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
        self.slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.slider.setTickInterval(2)
        self.slider.valueChanged.connect(self.filter_slided)
        self.show()


    def clicker(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "D://OFVS//videos","JPG Files (*.jpg);;PNG Files(*.png)")
        if fname:
            self.entry.setText(fname[0])


    def clicker2(self):
        fname2 = QFileDialog.getSaveFileName(self, "Set File Name", "D://OFVS//output","TXT Files (*.txt)" )
        if fname2:
            self.entry2.setText(fname2[0])

    def clicker3(self):
        if self.entry.text() and self.entry2.text():
            convert2text(self.entry.text(), self.entry2.text())

    ###############
    def clicker5(self):
        global fname3
        fname3 = QFileDialog.getOpenFileName(self, "Open File", "D://OFVS//videos","JPG Files (*.jpg);;PNG Files(*.png)")
        self.pixmap3 = QPixmap(fname3[0])
        self.label15.setPixmap(self.pixmap3.scaled(self.label15.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))


    def brightness_slided(self,value):
        inp = cv2.imread(fname3[0],cv2.COLOR_BGR2RGB)
        brightness = self.bright_slider.value()
        alpha = 1 + brightness/100 
        beta =  0
        out = cv2.convertScaleAbs(inp, alpha=alpha, beta=beta)
        height, width, channel = out.shape
        bytes_per_line = channel * width
        q_image = QImage(out.data,width, height, bytes_per_line, QImage.Format.Format_BGR888)
        self.pixmap4 = QPixmap.fromImage(q_image)
        self.label16.setPixmap(self.pixmap4.scaled(self.label16.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.bright_slider.setValue(value)
        self.label18.setText(str(value))

    ##############
    def clicker7(self):
        global fname6
        fname6 = QFileDialog.getOpenFileName(self, "Open File", "D://OFVS//videos","JPG Files (*.jpg);;PNG Files(*.png)")
        self.pixmap1 = QPixmap(fname6[0])
        self.label7.setPixmap(self.pixmap1.scaled(self.label7.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def filter_slided(self,value):
        inp = cv2.imread(fname6[0],cv2.COLOR_BGR2RGB)
        if value % 2 == 0:
            value = value - 1 if value > self.slider.value() else value + 1
        self.slider.setValue(value)
        if fname6:
            if filter_type == "Median Filter":
                out = cv2.medianBlur(inp,value)
            elif filter_type == "Gaussian Filter":
                out = cv2.GaussianBlur(inp,(value,value),0)
            elif filter_type == "Box Filter":
                out = cv2.blur(inp,(value,value))
            elif filter_type == "NL Means":
                out = cv2.fastNlMeansDenoisingColored(inp,None,value,value,7,21)
            height, width, channel = out.shape
            bytes_per_line = channel * width
            q_image = QImage(out.data,width, height, bytes_per_line, QImage.Format.Format_BGR888)
            self.pixmap2 = QPixmap.fromImage(q_image)
            self.label8.setPixmap(self.pixmap2.scaled(self.label8.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.label12.setText(str(value))

# Đọc dữ liệu từ file văn bản


def convert2text(input_image_filename,output_text_filename):
# Mở ảnh và chuyển sang chế độ thang xám nếu cần
    image = Image.open(input_image_filename).convert("L")  # "L" để chuyển sang grayscale

    # Lấy kích thước ảnh
    width, height = image.size

    # Mở file đầu ra để ghi dữ liệu
    with open(output_text_filename, 'w') as file:
        # Ghi chiều rộng và chiều dài của ảnh vào hai dòng đầu tiên
        file.write(format(width, '016b') + '\n')
        file.write(format(height, '016b') + '\n')
        
        # Duyệt qua từng pixel trong ảnh và ghi giá trị nhị phân 16-bit của mỗi pixel
        for y in range(height):
            for x in range(width):
                pixel_value = image.getpixel((x, y))
                # Chuyển giá trị pixel sang nhị phân 16-bit
                binary_value = format(pixel_value, '016b')
                # Ghi mỗi giá trị nhị phân trên một dòng
                file.write(binary_value + '\n')
    print(f"Dữ liệu đã được lưu thành {output_text_filename}")

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec()
