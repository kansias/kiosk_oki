
import sys
import cv2
import numpy as np
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import QTimer
from ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Init face cascade
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        # Start video capture
        self.cap = cv2.VideoCapture(0)
        
        # cam size 320x240
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        # cam mirror
        # Check if video capture is successful
        if not self.cap.isOpened():
            print("Failed to open webcam.")
            sys.exit()
        
        # Set a timer to fetch frames from the webcam
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Fetch frame every 30ms
        
        # Load and add menu images to grid layout
        self.menu_image_paths = ["./img/001.jpg", "./img/002.jpg"]
        for index, img_path in enumerate(self.menu_image_paths):
            pixmap = QPixmap(img_path)
            
            # Resize the pixmap based on window resolution
            width = self.width()
            if width < 800:
                pixmap = pixmap.scaled(200, 200)
            elif width > 1200:
                pixmap = pixmap.scaled(300, 300)
            else:
                pixmap = pixmap.scaled(250, 250)
            
            label = QLabel(self)
            label.setPixmap(pixmap)
            label.setStyleSheet(u"QWidget {\n"
                                "    \n"
                                "    background-color: rgb(255, 255, 255);\n"
                                "    border: 2px solid rgb(60, 60, 60);\n"
                                "    border-radius: 3px;\n"
                                "}")
            label.setFixedSize(pixmap.size())  # Set fixed size for the label
            row = index // 2  
            col = index % 2
            
            self.gridLayout.addWidget(label, row, col)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # flip image
            frame = cv2.flip(frame, 1)
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray,  1.1 , 5) # detecMultiScale(image, scaleFactor, minNeighbors)
            
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                
            height, width, channel = frame.shape
            step = channel * width
            qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(qImg))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

