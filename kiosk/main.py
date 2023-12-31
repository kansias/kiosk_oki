import keyword
import re
import sys
# import typing
# sys.path.append('kiosk')

from math import e
import time
import cv2
import numpy as np
import pyaudio
import wave
import openai
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QTextEdit
from PySide2.QtCore import Qt
from PySide2.QtCore import QTimer, Signal
from ui import QThread, Ui_MainWindow
import serial
import serial.tools.list_ports
from konlpy.tag import Okt
from openai.api_resources import file
# import tts module with pyside2
from gtts import gTTS
import pygame

import os
from dotenv import load_dotenv

try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
        
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # full screen
        # self.showFullScreen()
        
        self.p = pyaudio.PyAudio() 
        
        # Init face cascade
        self.face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
        
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
        # Init menu
        self.menu_dict = {"마이쮸": "./img/001.png", 
                            "ABC 초콜릿": "./img/002.png", 
                            '아이스 아메리카노': "./img/003.png",
                            '화이트 하임' : "./img/004.png"
                        }
        
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
        
        self.menu_image_paths = ["./img/001.png", "./img/002.png", "./img/003.png", "./img/004.png" ]
        self.add_widgets(self.gridLayout, self.menu_image_paths)
        
        self.new_window = NewWindow()
        self.new_window.show()
        
    def add_widgets(self, gridLayout, menu_image_paths, scale1=200, scale2=250, scale3=300):
        # Load and add menu images to grid layout
        for index, img_path in enumerate(menu_image_paths):
            pixmap = QPixmap(img_path)
            
            # Resize the pixmap based on window resolution
            width = self.width()
            if width < 1300:
                pixmap = pixmap.scaled(scale1, scale1)
            elif width <= 1700:
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
            row = index // 2  
            col = index % 2
            
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
            self.faces = self.face_cascade.detectMultiScale(gray,  1.2 , 3) # detecMultiScale(image, scaleFactor, minNeighbors)
            
            if len(self.faces) > 0:
                if self.status == 'wait':
                    self.status = 'order'
                    
                    self.ment_label.setText("(...인식중...)<br>주문하실 메뉴를 말씀해주세요")
                    self.ment_label.adjustSize()
                    self.delete_all_widgets(self.gridLayout_2)  # 주문내역 위젯에 있는 모든 이미지 삭제
                    
                    # thread tts
                    self.thread_tts = thread_tts("주문 하실 메뉴를 말씀해주세요")
                    self.thread_tts.start()
                
                    self.thread_start_recording.start()
                    QTimer.singleShot(7000, self.transcribe_audio)
                    
                elif self.status == 'reorder':
                    self.status = 'order'
                    
                    self.ment_label.setText("(...인식중...)<br>주문하신 메뉴가 없습니다<br>다시 주문해주세요<br>")
                    self.ment_label.adjustSize()
                    self.delete_all_widgets(self.gridLayout_2)  # 주문내역 위젯에 있는 모든 이미지 삭제
                    
                    # thread tts
                    self.thread_tts = thread_tts("주문 하실 메뉴를 말씀해주세요")
                    self.thread_tts.start()
                    
                    self.thread_start_recording.start()
                    QTimer.singleShot(8000, self.transcribe_audio) # 8초
                    
            if self.status == 'pay':
                self.status = 'paying'
                self.thread_start_recording.start()
                QTimer.singleShot(10000, self.transcribe_audio)  # 10초
                
            for (x,y,w,h) in self.faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,67,0),2)
                
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
                self.new_window.set_menu_list(self.final_order)
            
            # 결제 하시겠습니까? -> 응답이 없거나 '아니요'라는 응답 시
            else:
                self.delete_all_widgets(self.gridLayout_2)  # 주문내역 위젯에 있는 모든 이미지 삭제
            
            # 10초뒤 status를 wait로 초기화
            self.timer.singleShot(10000, self.initialize_status)
            
    def parse_menu(self, transcript):
        menu_order = []
        
        if ("마이" in transcript and "쮸" in transcript) or ("말쭈" in transcript):
            menu_order.append("마이쮸")
        if "ABC" in transcript or "초콜릿" in transcript:
            menu_order.append("ABC 초콜릿")
        if "아이스" in transcript or "아메리카노" in transcript:
            menu_order.append("아이스 아메리카노")
        if "화이트" in transcript or "하임" in transcript or "화이트하임" in transcript or "화이트아임" in transcript  :
            menu_order.append("화이트 하임")
        if "올려줘" in transcript or "올려주세요" in transcript:
            arduino.write(b'U')
        if "내려줘" in transcript or "내려주세요" in transcript:
            arduino.write(b'D')
            
            
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
            self.ment_label.setText(f"(...인식중...)<br>주문하신 메뉴는<br>'{order_text}'입니다.<br>주문을 진행하시겠습니까?")
            self.ex_label.setText(f"예 / 아니오")
            self.ment_label.adjustSize()
            # thread tts
            self.thread_tts = thread_tts(f"주문하신 메뉴는 {order_text}입니다. 주문을 진행하시겠습니까?")
            self.thread_tts.start()
            
            self.add_widgets(self.gridLayout_2, menu_image_paths, scale1=80, scale2=90, scale3=100)  # 주문내역 위젯에 이미지 추가
            return True

    def parse_answer(self, transcript):
        keywords = ["네", "응", "예", "어", "그래", "yeah"]
        if any(keyword in transcript for keyword in keywords):
            self.ment_label.setText("주문이 완료 되었습니다<br>감사합니다.")
            self.ment_label.adjustSize()
            # thread stt
            self.thread_tts = thread_tts("주문이 완료 되었습니다. 감사합니다.")
            self.thread_tts.start()
                        
            return True
        else:
            self.ment_label.setText("주문을 취소합니다<br>다시 주문해주세요")
            self.ment_label.adjustSize()
            # thread stt
            self.thread_tts = thread_tts("주문을 취소합니다. 다시 주문해주세요")
            self.thread_tts.start()
            
            return False
        
    # def play_and_remove_tts(self, text, lang='ko'):
    #     # gTTS를 사용하여 텍스트를 mp3로 변환
    #     tts = gTTS(text=text, lang=lang)
    
    #     # 프로젝트 디렉토리에 임시 파일 생성
    #     temp_file_path = os.path.join(os.getcwd(), "temp_tts.mp3")
        
    #     # mp3 파일 저장
    #     tts.save(temp_file_path)
        
    #     # mp3 파일 재생
    #     pygame.init()
    #     pygame.mixer.init()
    #     pygame.mixer.music.load(temp_file_path)
    #     pygame.mixer.music.play()
        
    #     # 오디오 재생이 완료될 때까지 대기
    #     while pygame.mixer.music.get_busy():
    #         pygame.time.Clock().tick(10) 
        
    #     # 재생이 완료되면 파일 제거
    #     pygame.mixer.quit()
        
    #     os.remove(temp_file_path)
        
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
        
        self.thread_start_recording.stream.stop_stream()
        self.thread_start_recording.stream.close()
        self.thread_start_recording.p.terminate()
        self.timer.stop()
        
        return super().closeEvent(event)
        
class thread_tts(QThread):
    def __init__(self, text, lang='ko'):
        super(thread_tts, self).__init__()
        self.text = text
        self.lang = lang
        
    def run(self):
        self.play_tts(self.text, self.lang)
        
    def stop(self):
        self.quit() #
        
    def play_tts(self, text, lang='ko'):
        # gTTS를 사용하여 텍스트를 mp3로 변환
        tts = gTTS(text=text, lang=lang)
    
        # 프로젝트 디렉토리에 임시 파일 생성
        temp_file_path = os.path.join(os.getcwd(), "temp_tts.mp3")
        
        # mp3 파일 저장
        tts.save(temp_file_path)
        
        # mp3 파일 재생
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(temp_file_path)
        pygame.mixer.music.play()
        
        # 오디오 재생이 완료될 때까지 대기
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10) 
        
        # 재생이 완료되면 파일 제거
        pygame.mixer.quit()
        
        os.remove(temp_file_path)
        self.stop()

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
            transcript = openai.Audio.transcribe("whisper-1", f, language="ko")
            
        self.text = transcript.text
        self.signal.emit(self.text)
        print('transcribe:', self.text)

class NewWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        # 주문 내역 출력할 텍스트 에디터
        
        # container
        self.container = QWidget()
        self.setCentralWidget(self.container)
        # background color
        self.container.setStyleSheet("background-color: #ffffff")
        
        # layout, center align
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.container.setLayout(self.layout)
        
        # title label
        self.title_label = QLabel()
        self.title_label.setText("주문 내역을 확인해주세요")
        self.title_label.setAlignment(Qt.AlignCenter)
        # font size
        self.title_label.setStyleSheet("font-size: 30px; font-weight: bold; color: #fd4500; ")
        
        # text label
        
        self.text_label = QLabel()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(False)
        self.text_edit.setStyleSheet("font-size: 20px; font-weight: bold")
        self.text_edit.setAlignment(Qt.AlignCenter)
        
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.text_label)
        self.layout.addWidget(self.text_edit)        
        
        
        # 주문 내역 출력
        self.text_label.setText("주문 접수 리스트")
        self.text_label.setAlignment(Qt.AlignCenter)
        # font size 
        self.text_label.setStyleSheet("font-size: 20px")
        self.text_label.adjustSize()
        
    def set_menu_list(self, order_menus):
        menu_text = ''
        for n, menus in enumerate(order_menus, start=1):
            menu_text += f'주문번호 : {n} <br>'
            for menu in menus:
                menu_text += f'{menu}<br>'
            menu_text += '<br>'
                
        self.text_edit.setText(menu_text)
        self.text_edit.setAlignment(Qt.AlignCenter)
        #font size, bold
        self.text_edit.setStyleSheet("font-size: 40px; font-weight: bold")
        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
