from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QSpinBox
from PyQt5.QtCore import QTimer, QTime, Qt, QPoint
import pygame
import sys
import os
pygame.mixer.init()
original_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')
sys.stdout = original_stdout

# Check if we're running as an executable
if getattr(sys, 'frozen', False):
    # If we are, set 'base_path' to the folder containing the executable
    base_path = sys._MEIPASS
else:
    # If we're not, set 'base_path' to the current working directory
    base_path = os.path.dirname(__file__)

# Use 'base_path' to locate 'alarm.wav'
sound_file = os.path.join(base_path, 'alarm.wav')
pygame.mixer.music.load(sound_file)

class CountdownForm(QWidget):
    def __init__(self):
        super().__init__()

        # make the window transparent and always on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()
        self.spin_box = QSpinBox()
        
        self.spin_box.setRange(1, 45)
        layout.addWidget(self.spin_box)

        self.label = QLabel()
        # set the color of the countdown timer to bright yellow and increase the font size
        self.label.setStyleSheet("color: yellow; font-size: 30px;font-family: 'Comic Sans MS'")
        layout.addWidget(self.label)

        self.start_button = QPushButton('Start Countdown')
        self.start_button.clicked.connect(self.start_countdown)
        layout.addWidget(self.start_button)

        self.setLayout(layout)
        self.timer = QTimer()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def start_countdown(self):
        # get the number of minutes from the spin box
        window.move(30, -50)
        minutes = self.spin_box.value()
        countdown_time = QTime(0, minutes, 0)
        
        def update_label():
            nonlocal countdown_time
            text = countdown_time.toString('mm:ss')
            self.label.setText(text)
            countdown_time = countdown_time.addSecs(-1)
            
            if countdown_time == QTime(0, 0):
                pygame.mixer.music.play()
                # stop the program after 7 seconds
                QTimer.singleShot(7000, app.quit)
                
        self.timer.timeout.connect(update_label)
        self.timer.start(1000)
        
        # hide the start button and spin box after the countdown starts
        self.start_button.hide()
        self.spin_box.hide()

app = QApplication([])
window = CountdownForm()
window.move(0, 0)  # set the window's start location
window.show()
app.exec_()
