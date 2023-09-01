import sys
sys.path.append('kiosk')

from math import e
import time
import cv2
import numpy as np
import pyaudio
import wave
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
openai.api_key = os.getenv("OPENAI_API_KEY")
        
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.p = pyaudio.PyAudio() 
        
        # Init face cascade
        self.face_cascade = cv2.CascadeClassifier('./kiosk/haarcascade_frontalface_default.xml')
        
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
        
        # Init menu
        self.menu_dict = {"마이쮸": "./kiosk/img/001.png", "ABC 초콜릿": "./kiosk/img/002.png", '아이스 아메리카노': "./kiosk/img/003.png"}
        self.menu_order = []
        self.final_order = []
        
        # Set the chunk size, sample format, channels, and rate
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 2
        self.rate = 44100
        
        # Define Thread
        self.status = 'wait'  # wait, order, reorder, pay, paying
        self.thread_start_recording = thread_start_recording(chunk=self.chunk, sample_format=self.sample_format, channels=self.channels, rate=self.rate)
        self.thread_transcribe_audio = thread_transcribe_audio()
        self.thread_transcribe_audio.signal.connect(self.get_transcription)

        if not self.cap.isOpened():
            print("Failed to open webcam.")
            sys.exit()
            
        if self.get_available_arduino_ports():
            self.comboBox.addItems(self.get_available_arduino_ports())
        else:
            self.comboBox.addItem("연결된 포트 없음")
            
        # Set a timer to fetch frames from the webcam
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Fetch frame every 30ms
        
        self.menu_image_paths = ["./kiosk/img/001.png", "./kiosk/img/002.png", "./kiosk/img/003.png"]
        self.add_widgets(self.gridLayout, self.menu_image_paths)
        
    def add_widgets(self, gridLayout, menu_image_paths, scale1=200, scale2=300, scale3=250):
        # Load and add menu images to grid layout
        for index, img_path in enumerate(menu_image_paths):
            pixmap = QPixmap(img_path)
            
            # Resize the pixmap based on window resolution
            width = self.width()
            if width < 800:
                pixmap = pixmap.scaled(scale1, scale1)
            elif width > 1200:
                pixmap = pixmap.scaled(scale2, scale2)
            else:
                pixmap = pixmap.scaled(scale3, scale3)

            
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
            
            gridLayout.addWidget(label, row, col)
    
    def delete_all_widgets(self, gridLayout):
        # remove all items from the layout list
        for i in reversed(range(gridLayout.count())): 
            widgetToRemove = gridLayout.itemAt(i).widget()
            gridLayout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
                    
    def initialize_status(self):
        self.status = 'wait'
        
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
                if self.status == 'wait':
                    self.status = 'order'
                    self.ment_label.setText("주문하실 메뉴를 말씀해주세요 (인식중)")
                    self.ment_label.adjustSize()

                    self.thread_start_recording.start()
                    QTimer.singleShot(5000, self.transcribe_audio)
                    
                elif self.status == 'reorder':
                    self.status = 'order'
                    self.ment_label.setText("주문하신 메뉴가 없습니다. 다시 주문해주세요 (인식중)")
                    self.ment_label.adjustSize()
                    
                    self.thread_start_recording.start()
                    QTimer.singleShot(5000, self.transcribe_audio)
                    
            if self.status == 'pay':
                self.status = 'paying'
                self.thread_start_recording.start()
                QTimer.singleShot(5000, self.transcribe_audio)
                
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

    def transcribe_audio(self):
        self.make_audio_file(self.thread_start_recording.frames)
        self.thread_start_recording.stop()
        
        self.ment_label.setText("잠시만 기다려주세요.")
        self.thread_transcribe_audio.start()
        
    def make_audio_file(self, frames):
        self.record = False
        filename = "output.wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    def get_transcription(self, text):
        if self.status == 'order':
            done = self.parse_menu(text)
            self.status = 'pay' if done else 'reorder'  # 주문 내역이 있으면 pay, 없으면 reorder
        
        elif self.status == 'paying':
            pay = self.parse_answer(text)
            
            # 결제 하시겠습니까? -> '네' 라는 응답 시
            if pay:
                self.final_order.append(self.menu_order)  # 최종 주문 내역에 추가
            
            # 결제 하시겠습니까? -> 응답이 없거나 '아니요'라는 응답 시
            else:
                self.delete_all_widgets(self.gridLayout_2)  # 주문내역 위젯에 있는 모든 이미지 삭제
            
            # 5초뒤 status를 wait로 초기화
            self.timer.singleShot(5000, self.initialize_status)
            
    def parse_menu(self, transcript):
        self.delete_all_widgets(self.gridLayout_2)  # 주문내역 위젯에 있는 모든 이미지 삭제
        menu_order = []
        
        if ("마이" in transcript and "쮸" in transcript) or ("말쭈" in transcript):
            menu_order.append("마이쮸")
        if "ABC" in transcript and "초콜릿" in transcript:
            menu_order.append("ABC 초콜릿")
        if "아이스" in transcript and "아메리카노" in transcript:
            menu_order.append("아이스 아메리카노")
            
        self.menu_order = menu_order
        
        # 주문 내역이 없을 시
        if len(menu_order) == 0:
            return False
        
        # 주문 내역이 있으면 주문 내역 출력
        else:
            order_text = ""
            menu_image_paths = []
            
            for menu in menu_order:
                order_text += menu + ", "  # 주문 내역 텍스트
                menu_image = self.menu_dict[menu]  # 메뉴 이미지
                menu_image_paths.append(menu_image)
                
            order_text = order_text[:-2]  # 마지막 ", " 제거
            self.ment_label.setText(f"주문하신 메뉴는 '{order_text}'입니다. 주문을 진행하시겠습니까?")
            self.ment_label.adjustSize()
            
            self.add_widgets(self.gridLayout_2, menu_image_paths, scale1=50, scale2=70, scale3=60)  # 주문내역 위젯에 이미지 추가
            
            return True

    def parse_answer(self, transcript):
        if "네" in transcript:
            self.ment_label.setText("주문이 완료 되었습니다. 주문 내역을 확인해주세요.")
            self.ment_label.adjustSize()
            return True
        else:
            self.ment_label.setText("주문을 취소합니다. 다시 주문해주세요.")
            self.ment_label.adjustSize()
            return False
        
    def closeEvent(self, event) -> None:
        self.cap.release()
        self.p.terminate()
        
        self.thread_start_recording.stream.stop_stream()
        self.thread_start_recording.stream.close()
        self.thread_start_recording.p.terminate()
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
        
        return self.frames

class thread_transcribe_audio(QThread):
    signal = Signal(str)
    
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
        self.signal.emit(self.text)
        print('transcribe:', self.text)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
