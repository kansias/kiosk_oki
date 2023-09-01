
from math import e
import sys
import time
import cv2
import numpy as np
import pyaudio
import wave
import threading
import openai
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import QTimer
from ui import QThread, Ui_MainWindow
import serial
import serial.tools.list_ports
from konlpy.tag import Okt
from openai.api_resources import file


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
        self.back_button.clicked.connect(self.backBtnClicked)
        self.option_Button.clicked.connect(self.optionBtnClicked)
        self.connect_button.clicked.connect(self.connectBtnClicked)
        
        # self.thread_start_recording = thread_start_recording()
        # self.thread_transcribe_audio = thread_transcribe_audio()
        
        self.record = False
        self.frames = []
        self.p = pyaudio.PyAudio()
        
        if not self.cap.isOpened():
            print("Failed to open webcam.")
            sys.exit()
            
        if self.get_available_arduino_ports():
            self.comboBox.addItems(self.get_available_arduino_ports())
        else:
            self.comboBox.addItem("연결된 포트 없음")
            
        self.frames = []
        openai.api_key = "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"
        # Set the chunk size, sample format, channels, and rate
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 2
        self.rate = 44100

        
        # Set a timer to fetch frames from the webcam
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Fetch frame every 30ms
        
        # Load and add menu images to grid layout
        self.menu_image_paths = ["./img/001.jpg", "./img/002.jpg", "./img/002.jpg", "./img/002.jpg", "./img/002.jpg"]
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
                                "    border: 1px solid rgb(100, 100, 100);\n"
                                "    border-radius: 3px;\n"
                                "}")
            label.setFixedSize(pixmap.size())  # Set fixed size for the label
            row = index // 3  
            col = index % 3
            
            self.gridLayout.addWidget(label, row, col)
    

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # flip image
            frame = cv2.flip(frame, 1)
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.faces = self.face_cascade.detectMultiScale(gray,  1.1 , 1) # detecMultiScale(image, scaleFactor, minNeighbors)
            
            if len(self.faces) > 0:
                self.record = True
                # self.thread_start_recording.start()
                # QTimer.singleShot(2000, self.make_audio_file)
                # self.start_recording()
            
            for (x,y,w,h) in self.faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                
            height, width, channel = frame.shape
            step = channel * width
            qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(qImg))
            
    def optionBtnClicked(self):
        self.stackedWidget.setCurrentIndex(1)
        
    def backBtnClicked(self):
        self.stackedWidget.setCurrentIndex(0)
                
    
    def get_available_arduino_ports(self):
        arduino_ports = []
        available_ports = list(serial.tools.list_ports.comports())
        for port in available_ports:
            arduino_ports.append(port.device)
        return arduino_ports
    
    def connectBtnClicked(self):
        global arduino
        arduino = serial.Serial(self.serial_port_combobox.currentText(), 9600)
        arduino.flush()
        # 연결되면 버튼 비활성화
        self.connect_button.setEnabled(False)
        self.combobox.setEnabled(False)
        # 연결됨으로 커넥트 버튼 텍스트 변경
        self.connect_button.setText("연결됨")
        
    def start_recording(self):
        self.ment_label.setText("주문하실 메뉴를 말씀해주세요(인식중)")
        self.ment_label.adjustSize()
        stream = self.p.open(format=self.sample_format, channels=self.channels, rate=self.rate, frames_per_buffer=self.chunk, input=True)        
        self.frames = []
        while self.record:
            data = stream.read(self.chunk)
            self.frames.append(data)
        stream.stop_stream()
        stream.close()
        
        return self.frames
    
    def make_audio_file(self):
        self.record = False
        filename = "output.wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        # self.thread_start_recording.stop()
        # self.thread_transcribe_audio.start()
        
    
    def transcribe_audio(self, filename):
        self.ment_label.setText("인식중...")
        with open(filename, 'rb') as f:
            transcript = openai.Audio.transcribe("whisper-1", f)
        result_text = transcript.text
        self.ment_label.setText("주문 내역을 확인해주세요.")
        self.ment_label.adjustSize()
        self.parse_transcript(result_text)
        
        
    def parse_transcript(self, transcript):
        okt = Okt()
        parsed_words = okt.nouns(transcript)
        # 중복 단어 제거
        parsed_words = list(set(parsed_words)) 
        
        menu_dict = {"마이쮸": "./img/001.jpg", "ABC 초콜릿": "./img/002.jpg", "./img/003.jpg": 3}
        menu_order = []
        
        for word in parsed_words:
            if "마이" in word and "쮸" in word:
                menu_order.append("마이쮸")
            elif word in menu_dict:
                menu_order.append(word)
            elif "ABC" in word and "초콜릿" in word:
                menu_order.append("ABC 초콜릿")
            elif "아이스" in word and "아메리카노" in word:
                menu_order.append("아이스 아메리카노")
        
        # 주문 내역 출력
        order_text = ""
        for menu in menu_order:
            order_text += menu + ", "
        order_text = order_text[:-2]  # 마지막 ", " 제거
        self.ment_label.setText(f"주문하신 메뉴는 '{order_text}'입니다. 주문을 진행하시겠습니까?")
        self.ment_label.adjustSize()
        
        

    def closeEvent(self, event) -> None:
        self.cap.release()
        self.p.terminate()
        self.timer.stop()
        
        
        return super().closeEvent(event)
        

# class thread_start_recording(QThread):
#     def __init__(self):
#         super(thread_start_recording, self).__init__()
#         self.main = MainWindow()

#     def run(self):
#         self.main.start_recording()
        
#     def stop(self):
#         self.main.record = False
#         self.quit()
# class thread_transcribe_audio(QThread):
#     def __init__(self):
#         super(thread_transcribe_audio, self).__init__()
#         self.main = MainWindow()

#     def run(self):
#         self.main.transcribe_audio("output.wav")
        
#     def stop(self):
#         self.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

