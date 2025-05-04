import sys
import threading
import time
import pyautogui
import cv2 # type: ignore
import numpy as np # type: ignore
import mss # type: ignore
import keyboard
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout,
    QWidget, QLabel, QHBoxLayout, QComboBox, QFrame
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

class FastGiftBot(threading.Thread):
    def __init__(self, speed=1.0):
        super().__init__()
        self.running = False
        self.speed = speed
        self.template1 = cv2.imread("1.png", cv2.IMREAD_GRAYSCALE)
        self.template5 = cv2.imread("5.png", cv2.IMREAD_GRAYSCALE)
        if self.template1 is None or self.template5 is None:
            print("خطأ: تعذر تحميل الصور (تأكد من وجود 1.png و 5.png)")
        self.w1, self.h1 = self.template1.shape[::-1]
        self.w5, self.h5 = self.template5.shape[::-1]
        self.threshold = 0.8

    def run(self):
        self.running = True
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            while self.running:
                sct_img = sct.grab(monitor)
                img = np.array(sct_img)
                gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
                
                for i in range(4):
                    if not self.running:
                        break
                    res1 = cv2.matchTemplate(gray, self.template1, cv2.TM_CCOEFF_NORMED)
                    loc1 = np.where(res1 >= self.threshold)
                    if len(loc1[0]) > 0:
                        pt = (loc1[1][0], loc1[0][0])
                        center = (pt[0] + self.w1 // 2, pt[1] + self.h1 // 2)
                        pyautogui.click(center[0], center[1])
                        print(f"تم النقر على 1.png في المحاولة {i+1}/4")
                        time.sleep(self.speed)
                    else:
                        print(f"لم يتم العثور على 1.png في المحاولة {i+1}/4")
                    time.sleep(self.speed)
                
                res5 = cv2.matchTemplate(gray, self.template5, cv2.TM_CCOEFF_NORMED)
                loc5 = np.where(res5 >= self.threshold)
                if len(loc5[0]) > 0:
                    pt = (loc5[1][0], loc5[0][0])
                    center = (pt[0] + self.w5 // 2, pt[1] + self.h5 // 2)
                    pyautogui.click(center[0], center[1])
                    print("تم النقر على 5.png")
                    time.sleep(self.speed)
                else:
                    print("لم يتم العثور على 5.png")
                time.sleep(self.speed)

    def stop(self):
        self.running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("بوت تجميع هدايا التحالف - 2025")
        self.setGeometry(100, 100, 600, 500)
        self.setMinimumSize(500, 400)
        self.bot = None
        self.current_speed = 1.0
        self.initUI()

    def initUI(self):
        # إنشاء إطار رئيسي مع خلفية شفافة
        main_frame = QFrame()
        main_frame.setObjectName("mainFrame")
        main_layout = QVBoxLayout(main_frame)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # عنوان التطبيق مع تأثير الظل
        title_frame = QFrame()
        title_frame.setObjectName("titleFrame")
        title_layout = QVBoxLayout(title_frame)
        
        title_label = QLabel("بوت تجميع هدايا التحالف")
        title_label.setObjectName("titleLabel")
        title_layout.addWidget(title_label)
        
        main_layout.addWidget(title_frame)
        
        # حالة البوت
        status_frame = QFrame()
        status_frame.setObjectName("statusFrame")
        self.status_label = QLabel("اضغط على 'تشغيل' لبدء بوت تجميع هدايا التحالف")
        self.status_label.setObjectName("statusLabel")
        status_layout = QVBoxLayout(status_frame)
        status_layout.addWidget(self.status_label)
        
        main_layout.addWidget(status_frame)
        
        # إطار التحكم
        control_frame = QFrame()
        control_frame.setObjectName("controlFrame")
        control_layout = QVBoxLayout(control_frame)
        
        # أزرار التحكم
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("تشغيل")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_bot)
        
        self.stop_button = QPushButton("إيقاف")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(self.stop_bot)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        control_layout.addLayout(button_layout)
        
        # اختيار السرعة
        speed_layout = QHBoxLayout()
        speed_label = QLabel("سرعة البوت:")
        speed_label.setObjectName("speedLabel")
        
        self.speed_combo = QComboBox()
        self.speed_combo.setObjectName("speedCombo")
        self.speed_combo.addItems(["0.0001 ثانية", "1 ثانية", "2 ثانية"])
        self.speed_combo.currentIndexChanged.connect(self.change_speed)
        
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_combo)
        control_layout.addLayout(speed_layout)
        
        main_layout.addWidget(control_frame)
        
        # إضافة مساحة مرنة
        main_layout.addStretch()
        
        # معلومات الاختصار
        shortcut_label = QLabel("اختصار الإيقاف السريع: Ctrl + Q")
        shortcut_label.setObjectName("shortcutLabel")
        main_layout.addWidget(shortcut_label, alignment=Qt.AlignCenter)
        
        self.setCentralWidget(main_frame)

    def change_speed(self):
        text = self.speed_combo.currentText()
        value_str = text.split()[0]
        try:
            self.current_speed = float(value_str)
        except ValueError:
            self.current_speed = 1.0
        if self.bot and self.bot.running:
            self.bot.speed = self.current_speed
        print(f"تم تغيير السرعة إلى {self.current_speed} ثانية")

    def start_bot(self):
        if self.bot is None or not self.bot.is_alive():
            self.bot = FastGiftBot(speed=self.current_speed)
            self.bot.start()
            self.status_label.setText("بوت تجميع هدايا التحالف قيد التشغيل...")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            print("البوت بدأ العمل.")

    def stop_bot(self):
        if self.bot and self.bot.running:
            self.bot.stop()
            self.status_label.setText("تم إيقاف بوت تجميع هدايا التحالف.")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            print("تم إيقاف البوت.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # تنسيق محسّن مع تأثيرات حديثة
    style = """
    QMainWindow {
        background: #1a1a1a;
    }
    
    #mainFrame {
        background: transparent;
    }
    
    #titleFrame {
        background: rgba(40, 40, 40, 0.7);
        border-radius: 15px;
        margin: 10px;
        padding: 20px;
    }
    
    #titleLabel {
        color: #ffffff;
        font-family: 'Cairo', sans-serif;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
    }
    
    #statusFrame {
        background: rgba(50, 50, 50, 0.7);
        border-radius: 10px;
        padding: 15px;
    }
    
    #statusLabel {
        color: #e0e0e0;
        font-family: 'Cairo', sans-serif;
        font-size: 18px;
        text-align: center;
    }
    
    #controlFrame {
        background: rgba(45, 45, 45, 0.7);
        border-radius: 15px;
        padding: 20px;
    }
    
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                  stop:0 #2196F3, stop:1 #1976D2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 30px;
        font-family: 'Cairo', sans-serif;
        font-size: 16px;
        font-weight: bold;
        min-width: 120px;
    }
    
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                  stop:0 #1E88E5, stop:1 #1565C0);
    }
    
    QPushButton:pressed {
        background: #0D47A1;
    }
    
    QPushButton:disabled {
        background: #666666;
        color: #999999;
    }
    
    #stopButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                  stop:0 #F44336, stop:1 #D32F2F);
    }
    
    #stopButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                  stop:0 #E53935, stop:1 #C62828);
    }
    
    #stopButton:pressed {
        background: #B71C1C;
    }
    
    QComboBox {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 6px;
        color: white;
        padding: 8px;
        min-width: 150px;
        font-family: 'Cairo', sans-serif;
        font-size: 14px;
    }
    
    QComboBox::drop-down {
        border: none;
        width: 30px;
    }
    
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid white;
        margin-right: 10px;
    }
    
    QComboBox QAbstractItemView {
        background: #2a2a2a;
        border: none;
        selection-background-color: #3a3a3a;
        selection-color: white;
        color: white;
    }
    
    #speedLabel {
        color: white;
        font-family: 'Cairo', sans-serif;
        font-size: 16px;
    }
    
    #shortcutLabel {
        color: #888888;
        font-family: 'Cairo', sans-serif;
        font-size: 14px;
    }
    """
    
    app.setStyleSheet(style)
    
    window = MainWindow()
    window.show()
    
    keyboard.add_hotkey('ctrl+q', lambda: window.stop_bot())
    
    sys.exit(app.exec_())