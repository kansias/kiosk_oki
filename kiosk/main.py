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
from PySide2.QtCore import QTimer, Signal
from ui import QThread, Ui_MainWindow
import serial
import serial.tools.list_ports
from konlpy.tag import Okt
from openai.api_resources import file

import os
from dotenv import load_dotenv
load_dotenv()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.p = pyaudio.PyAudio() 
        
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
        self.option_button.clicked.connect(self.optionBtnClicked)
        self.connect_button.clicked.connect(self.connectBtnClicked)
        
        self.LU_button.clicked.connect(self.clicked_LU_btn)
        self.LD_button.clicked.connect(self.clicked_LD_btn)
        self.RU_button.clicked.connect(self.clicked_RU_btn)
        self.RD_button.clicked.connect(self.clicked_RD_btn)
        self.AU_button.clicked.connect(self.clicked_AU_btn)
        self.AD_button.clicked.connect(self.clicked_AD_btn)
        
        # frame_6 disable
        self.frame_6.setEnabled(False)
        
        # Set the chunk size, sample format, channels, and rate
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 2
        self.rate = 44100
        self.complete_record = False
        
        self.thread_start_recording = thread_start_recording(chunk=self.chunk, sample_format=self.sample_format, channels=self.channels, rate=self.rate)
        self.thread_transcribe_audio = thread_transcribe_audio()

        if not self.cap.isOpened():
            print("Failed to open webcam.")
            sys.exit()
            
        if self.get_available_arduino_ports():
            self.comboBox.addItems(self.get_available_arduino_ports())
        else:
            self.comboBox.addItem("연결된 포트 없음")
            
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Set a timer to fetch frames from the webcam
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Fetch frame every 30ms
        
        # Load and add menu images to grid layout
        self.menu_image_paths = ["./img/001.png", "./img/002.png", "./img/003.png"]
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
                if not self.complete_record:
                    self.complete_record = True
                    self.ment_label.setText("주문하실 메뉴를 말씀해주세요(인식중)")
                    self.ment_label.adjustSize()

                    self.thread_start_recording.start()
                    QTimer.singleShot(7000, self.make_audio_file)
            
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
        arduino = serial.Serial(self.comboBox.currentText(), 9600)
        arduino.flush()
        # frame_6 enable
        self.frame_6.setEnabled(True)
        # 연결되면 버튼 비활성화
        self.connect_button.setEnabled(False)
        self.comboBox.setEnabled(False)
        # 연결됨으로 커넥트 버튼 텍스트 변경
        self.connect_button.setText("연결됨")

    def make_audio_file(self):
        self.record = False
        filename = "output.wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.thread_start_recording.frames))
        wf.close()
        
        self.thread_start_recording.stop()
        self.transcribe_audio(filename)
    
    def transcribe_audio(self, filename):
        self.ment_label.setText("인식중...")
        self.thread_transcribe_audio.transcribe_audio(filename)
        result_text = self.thread_transcribe_audio.text
        self.ment_label.setText("주문 내역을 확인해주세요.")
        self.ment_label.adjustSize()
        self.parse_transcript(result_text)
        
    def parse_transcript(self, transcript):
        # okt = Okt()
        # parsed_words = okt.nouns(transcript)
        # 중복 단어 제거
        # parsed_words = list(set(parsed_words)) 
        
        menu_dict = {"마이쮸": "./img/001.png", "ABC 초콜릿": "./img/002.png", '아이스 아메리카노' :"./img/003.png"}
        menu_order = []
        
        # for word in parsed_words:
        #     if "마이" in word and "쮸" in word:
        #         menu_order.append("마이쮸")
        #     elif word in menu_dict:
        #         menu_order.append(word)
        #     elif "ABC" in word and "초콜릿" in word:
        #         menu_order.append("ABC 초콜릿")
        #     elif "아이스" in word and "아메리카노" in word:
        #         menu_order.append("아이스 아메리카노")
        
        if "마이" in transcript and "쮸" in transcript:
            menu_order.append("마이쮸")
        if "ABC" in transcript and "초콜릿" in transcript:
            menu_order.append("ABC 초콜릿")
        if "아이스" in transcript and "아메리카노" in transcript:
            menu_order.append("아이스 아메리카노")
            
        for item in menu_order:
            if item in menu_dict:
                menu_order.append(transcript)
    
        # 주문 내역 출력
        order_text = ""
        for menu in menu_order:
            order_text += menu + ", "
        order_text = order_text[:-2]  # 마지막 ", " 제거
        self.ment_label.setText(f"주문하신 메뉴는 '{order_text}'입니다. 주문을 진행하시겠습니까?")
        self.ment_label.adjustSize()
        
    def clicked_LU_btn(self):
        arduino.write(b'7')
        print("LU")
    
    def clicked_LD_btn(self):
        arduino.write(b'1')
        print("LD")
        
    def clicked_RU_btn(self):
        arduino.write(b'8')
        print("RU")
        
    def clicked_RD_btn(self):
        arduino.write(b'2')
        print("RD")
    
    def clicked_AU_btn(self):
        arduino.write(b'9')
        print("AU")
    
    def clicked_AD_btn(self):
        arduino.write(b'3')
        print("AD")
        
    def closeEvent(self, event) -> None:
        self.cap.release()
        self.p.terminate()
        self.timer.stop()
        
        return super().closeEvent(event)
        

class thread_start_recording(QThread):    
    def __init__(self, sample_format, channels, rate, chunk):
        super(thread_start_recording, self).__init__()
        self.chunk = chunk
        self.record = False
        
        self.p = pyaudio.PyAudio() 
        self.stream = self.p.open(format=sample_format, channels=channels, rate=rate, frames_per_buffer=chunk, input=True)       
        self.frames = []

    def run(self):
        self.record = True
        self.start_recording()
        
    def stop(self):
        self.record = False
        
    def start_recording(self):
        self.frames = []
        while self.record:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
        # self.stream.stop_stream()
        # self.stream.close()
        
        return self.frames
    
class thread_transcribe_audio(QThread):
    def __init__(self):
        super(thread_transcribe_audio, self).__init__()
        self.text = None

    def run(self):
        self.transcribe_audio("output.wav")
        
    def stop(self):
        self.quit()

    def transcribe_audio(self, filename):
        with open(filename, 'rb') as f:
            transcript = openai.Audio.transcribe("whisper-1", f)
        self.text = transcript.text
        print('transcribe:', self.text)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
