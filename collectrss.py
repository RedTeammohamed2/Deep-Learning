import sys
import os
import random
import math
import time
import cv2
import numpy as np
import pyautogui
import keyboard
from collections import namedtuple
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel,
    QVBoxLayout, QWidget, QRubberBand, QHBoxLayout,
    QCheckBox, QGroupBox, QGridLayout, QScrollArea, QLineEdit
)
from PyQt5.QtCore import QThread, pyqtSignal, QRect, QSize, Qt
from PyQt5.QtGui import QPainter, QColor, QFont

# تعريف كائنات بسيطة للإحداثيات والصناديق
Point = namedtuple("Point", ["x", "y"])
Box = namedtuple("Box", ["left", "top", "width", "height"])

# ===========================================================
# خيط البوت – يستخدم OpenCV للبحث عن الصور وتنفيذ العملية
# ===========================================================
class MouseBotThread(QThread):
    updateStatus = pyqtSignal(str)

    resource_colors = {
        "قمح": "#FFD700",
        "حجر": "#A9A9A9",
        "خشب": "#8B4513",
        "معدن": "#4682B4",
        "دهب": "#FFD700",
        "جواهر": "#9400D3"
    }

    def __init__(self, region=None, resources=None, repeat_count=1, parent=None, step_distance=300):
        super(MouseBotThread, self).__init__(parent)
        self.running = False
        self.region = region
        self.resources = resources or []
        self.repeat_count = repeat_count  # عدد تكرار العملية بالكامل
        self.step_distance = step_distance
        # مسار المجلد الذي يحتوي على الصور
        self.base_path = r"C:\Project bot lord mobile Update v1.1 - Copy - Copy - Copy\images\Collectrss\\"
        self.food_img = os.path.join(self.base_path, "food.png")

    def run(self):
        """
        يبحث الخيط باستخدام OpenCV عن صورة food.png.
        عند العثور عليها:
         - يضغط عليها،
         - ينتظر قليلاً لتحديث الشاشة،
         - ثم يبحث عن الصور الإضافية (1.png، 2.png، 3.png) مع فترة انتظار تصل لـ10 ثوانٍ لكل صورة.
        تُكرر العملية بالكامل حسب قيمة repeat_count.
        """
        self.running = True
        iteration = 0
        while self.running and iteration < self.repeat_count:
            # انتظار حتى العثور على food.png
            while self.running:
                if "قمح" in self.resources:
                    location = self.find_image_center(self.food_img, threshold=0.8)
                    if location is not None:
                        self.click_at(location, desc="food.png")
                        self.updateStatus.emit("تم العثور على صورة food.png والضغط عليها.")
                        time.sleep(1)  # تأخير لتحديث الشاشة
                        self.process_extra_images()  # معالجة الصور الإضافية
                        break  # انتهاء التكرار الحالي عند العثور على food.png
                    else:
                        self.perform_random_movement()
                else:
                    self.perform_random_movement()
                self.msleep(300)
            iteration += 1
            self.updateStatus.emit(f"تم الانتهاء من التكرار رقم {iteration}.")
            time.sleep(1)  # فترة انتظار بين التكرارات (يمكن تعديلها)
        self.updateStatus.emit("اكتملت جميع التكرارات.")

    def find_image_center(self, image_path, threshold=0.8):
        """
        يلتقط صورة للشاشة ويبحث عن مركز الصورة المطلوبة باستخدام OpenCV.
        يُرجع كائن Point (x, y) إذا تم العثور عليها، أو None.
        """
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        template = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if template is None:
            self.updateStatus.emit(f"غير قادر على قراءة الصورة {os.path.basename(image_path)}")
            return None
        w, h = template.shape[1], template.shape[0]
        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        if len(loc[0]) == 0:
            return None
        pt = (int(loc[1][0]), int(loc[0][0]))
        return Point(pt[0] + w // 2, pt[1] + h // 2)

    def find_all_locations(self, image_path, threshold=0.6):
        """
        يلتقط صورة للشاشة ويبحث عن كل مواقع ظهور الصورة المطلوبة باستخدام OpenCV.
        يُرجع قائمة من كائنات Box.
        """
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        template = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if template is None:
            self.updateStatus.emit(f"غير قادر على قراءة الصورة {os.path.basename(image_path)}")
            return []
        w, h = template.shape[1], template.shape[0]
        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        boxes = []
        for pt in zip(*loc[::-1]):  # pt هو (x, y)
            boxes.append(Box(left=pt[0], top=pt[1], width=w, height=h))
        return boxes

    def click_at(self, point, desc=""):
        """
        ينفذ نقرة عند النقطة المحددة.
        """
        try:
            pyautogui.click(point.x, point.y)
            self.updateStatus.emit(f"تم الضغط على {desc} في النقطة ({point.x}, {point.y}).")
        except Exception as e:
            self.updateStatus.emit(f"خطأ أثناء الضغط عند {desc}: {e}")

    def process_extra_images(self):
        """
        يبحث عن الصور الإضافية (1.png، 2.png، 3.png) باستخدام OpenCV وينفذ النقر على أول ظهور لكل صورة.
        لكل صورة يستمر البحث لمدة 10 ثوانٍ قبل الانتقال إذا لم تُعثر عليها.
        نستخدم قيمة ثقة 0.8 للصورة 2.png وبقية الصور 0.6.
        """
        for i in range(1, 4):
            img_path = os.path.join(self.base_path, f"{i}.png")
            self.updateStatus.emit(f"يتم معالجة الصورة {i}.png...")
            conf = 0.8 if i == 2 else 0.6
            start_time = time.time()
            found = False
            while time.time() - start_time < 10:
                locations = self.find_all_locations(img_path, threshold=conf)
                if locations:
                    box = locations[0]  # الضغط على أول ظهور فقط
                    center = Point(box.left + box.width // 2, box.top + box.height // 2)
                    self.click_at(center, desc=f"{i}.png")
                    self.updateStatus.emit(f"تم الضغط على الصورة {i}.png.")
                    found = True
                    break
                time.sleep(0.5)
            if not found:
                self.updateStatus.emit(f"لم يتم العثور على الصورة {i}.png بعد الانتظار.")

    def perform_random_movement(self):
        """
        ينفذ حركة سحب عشوائية في المنطقة المحددة أو في مركز الشاشة.
        """
        if self.region is None:
            screenWidth, screenHeight = pyautogui.size()
            center_x = screenWidth // 2
            center_y = screenHeight // 2
        else:
            center_x = self.region.x() + self.region.width() // 2
            center_y = self.region.y() + self.region.height() // 2

        pyautogui.moveTo(center_x, center_y, duration=0.01)
        angle = random.uniform(0, 2 * math.pi)
        target_x = int(center_x + self.step_distance * math.cos(angle))
        target_y = int(center_y + self.step_distance * math.sin(angle))
        substeps = 10
        pyautogui.mouseDown()
        for step in range(1, substeps + 1):
            intermediate_x = int(center_x + (target_x - center_x) * step / substeps)
            intermediate_y = int(center_y + (target_y - center_y) * step / substeps)
            try:
                pyautogui.moveTo(intermediate_x, intermediate_y, duration=0.005)
            except Exception as e:
                self.updateStatus.emit(f"خطأ أثناء الحركة العشوائية: {e}")
        pyautogui.mouseUp()
        pyautogui.moveTo(center_x, center_y, duration=0.01)
        if self.resources:
            current_resource = random.choice(self.resources)
            self.updateStatus.emit(f"جاري جمع: {current_resource}")

    def stop(self):
        self.running = False

    def quit(self):
        self.running = False
        super().quit()


# ===========================================================
# واجهة اختيار المنطقة
# ===========================================================
class RegionSelector(QWidget):
    regionSelected = pyqtSignal(QRect)

    def __init__(self):
        super(RegionSelector, self).__init__()
        self.setWindowTitle("تحديد منطقة البحث")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.showFullScreen()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.origin = None
        self.selectionRect = QRect()
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.selectionRect = QRect(self.origin, QSize())
            self.rubberBand.setGeometry(self.selectionRect)
            self.rubberBand.show()

    def mouseMoveEvent(self, event):
        if self.origin:
            self.selectionRect = QRect(self.origin, event.pos()).normalized()
            self.rubberBand.setGeometry(self.selectionRect)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rubberBand.hide()
            self.regionSelected.emit(self.selectionRect)
            self.close()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))
        if not self.selectionRect.isNull():
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(self.selectionRect, QColor(0, 0, 0, 0))


# ===========================================================
# الواجهة الرئيسية للتطبيق
# ===========================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.selected_region = None
        self.selected_resources = []
        self.botThread = None
        self.setFixedSize(650, 800)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint & ~Qt.WindowMinimizeButtonHint)
        self.initUI()
        self.setup_styles()

    def initUI(self):
        self.arabic_font = QFont("Cairo", 10)
        self.arabic_font.setBold(True)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # الهيدر
        header_layout = QHBoxLayout()
        logo_label = QLabel("🤖")
        logo_label.setFont(QFont("Arial", 24))
        logo_label.setFixedSize(60, 60)
        title = QLabel("بوت جمع الموارد الذكي")
        title.setFont(QFont("Cairo", 18, QFont.Bold))
        title.setFixedHeight(60)
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title)
        header_layout.setAlignment(Qt.AlignCenter)

        # قسم الموارد
        resource_group = QGroupBox("اختيار الموارد المطلوبة")
        resource_group.setFont(QFont("Cairo", 12))
        resource_group.setFixedHeight(250)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(200)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { width: 8px; background: #f0f0f0; border-radius: 4px; }
            QScrollBar::handle:vertical { background: #c0c0c0; min-height: 30px; border-radius: 4px; }
        """)
        resource_content = QWidget()
        resource_layout = QGridLayout()
        resource_layout.setContentsMargins(10, 10, 10, 10)
        resource_layout.setHorizontalSpacing(15)
        resource_layout.setVerticalSpacing(10)
        self.resource_checkboxes = {
            "قمح": self.create_resource_button("قمح", "🌾", "#f1c40f"),
            "حجر": self.create_resource_button("حجر", "⛰️", "#7f8c8d"),
            "خشب": self.create_resource_button("خشب", "🌲", "#8b4513"),
            "معدن": self.create_resource_button("معدن", "⚙️", "#95a5a6"),
            "دهب": self.create_resource_button("ذهب", "💰", "#f39c12"),
            "جواهر": self.create_resource_button("جواهر", "💎", "#9b59b6")
        }
        row, col = 0, 0
        for resource, checkbox in self.resource_checkboxes.items():
            checkbox.setFixedSize(170, 50)
            resource_layout.addWidget(checkbox, row, col)
            col = (col + 1) % 3
            if col == 0:
                row += 1
        resource_content.setLayout(resource_layout)
        scroll.setWidget(resource_content)
        resource_group.setLayout(QVBoxLayout())
        resource_group.layout().addWidget(scroll)

        # لوحة التحكم مع خانة عدد التكرار
        control_panel = QGroupBox("لوحة التحكم")
        control_panel.setFont(QFont("Cairo", 12))
        control_panel.setFixedHeight(150)
        control_layout = QVBoxLayout()
        repeat_layout = QHBoxLayout()
        repeat_label = QLabel("عدد التكرار:")
        repeat_label.setFont(QFont("Cairo", 10))
        self.repeatEdit = QLineEdit("5")
        self.repeatEdit.setFixedWidth(50)
        repeat_layout.addWidget(repeat_label)
        repeat_layout.addWidget(self.repeatEdit)
        repeat_layout.addStretch()
        button_layout = QHBoxLayout()
        self.selectRegionButton = self.create_control_button("تحديد المنطقة", "🎯", "#3498db", 180, 45)
        self.startButton = self.create_control_button("تشغيل", "▶️", "#2ecc71", 120, 45)
        self.stopButton = self.create_control_button("إيقاف", "⏹️", "#e74c3c", 120, 45)
        button_layout.addWidget(self.selectRegionButton)
        button_layout.addWidget(self.startButton)
        button_layout.addWidget(self.stopButton)
        control_layout.addLayout(repeat_layout)
        control_layout.addLayout(button_layout)
        control_panel.setLayout(control_layout)

        # معلومات التشغيل
        info_panel = QGroupBox("معلومات التشغيل")
        info_panel.setFont(QFont("Cairo", 12))
        info_panel.setFixedHeight(300)
        info_layout = QVBoxLayout()
        self.regionLabel = QLabel("🎯 المنطقة: غير محددة")
        self.regionLabel.setFont(self.arabic_font)
        self.regionLabel.setStyleSheet("padding: 8px; background: #ecf0f1; border-radius: 5px;")
        self.regionLabel.setFixedHeight(50)
        self.statusLabel = QLabel("⚪ الحالة: جاهز للتشغيل")
        self.statusLabel.setFont(self.arabic_font)
        self.statusLabel.setStyleSheet("padding: 8px; background: #ecf0f1; border-radius: 5px;")
        self.statusLabel.setFixedHeight(50)
        self.noteLabel = QLabel("📢 ملاحظة: اضغط Ctrl لإيقاف التشغيل الطارئ")
        self.noteLabel.setFont(QFont("Cairo", 10))
        self.noteLabel.setStyleSheet("""
            padding: 8px;
            background: #fff3cd;
            border-radius: 5px;
            color: #856404;
            border: 1px solid #ffeeba;
        """)
        self.noteLabel.setFixedHeight(40)
        self.noteLabel.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(self.regionLabel)
        info_layout.addWidget(self.statusLabel)
        info_layout.addWidget(self.noteLabel)
        info_panel.setLayout(info_layout)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(resource_group)
        main_layout.addWidget(control_panel)
        main_layout.addWidget(info_panel)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.selectRegionButton.clicked.connect(self.selectRegion)
        self.startButton.clicked.connect(self.startBot)
        self.stopButton.clicked.connect(self.stopBot)

    def create_resource_button(self, text, icon, color):
        checkbox = QCheckBox(f"{icon} {text}")
        checkbox.setFont(QFont("Cairo", 10))
        checkbox.setStyleSheet(f"""
            QCheckBox {{
                background-color: #ffffff;
                border: 2px solid {color};
                border-radius: 6px;
                padding: 8px 12px;
            }}
            QCheckBox:checked {{
                background-color: {color};
                color: white;
            }}
            QCheckBox:hover {{
                background-color: {color}22;
            }}
        """)
        return checkbox

    def create_control_button(self, text, icon, color, width, height):
        button = QPushButton(f"{icon} {text}")
        button.setFont(QFont("Cairo", 10))
        button.setFixedSize(width, height)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
            QPushButton:pressed {{
                background-color: {color}aa;
            }}
        """)
        return button

    def setup_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f8f9fa; }
            QGroupBox {
                border: 2px solid #e9ecef;
                border-radius: 12px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                color: #2c3e50;
            }
        """)

    def update_resources(self):
        self.selected_resources = [
            resource for resource, checkbox in self.resource_checkboxes.items()
            if checkbox.isChecked()
        ]

    def selectRegion(self):
        self.regionSelector = RegionSelector()
        self.regionSelector.regionSelected.connect(self.onRegionSelected)
        self.regionSelector.show()

    def onRegionSelected(self, rect):
        self.selected_region = rect
        self.regionLabel.setText(
            f"🚩 المنطقة الحالية: X={rect.x()} Y={rect.y()} "
            f"العرض={rect.width()} الارتفاع={rect.height()}"
        )

    def startBot(self):
        self.update_resources()
        try:
            repeat_count = int(self.repeatEdit.text())
        except ValueError:
            repeat_count = 1
        if self.botThread is None or not self.botThread.isRunning():
            self.botThread = MouseBotThread(region=self.selected_region, resources=self.selected_resources, repeat_count=repeat_count)
            self.botThread.updateStatus.connect(self.onUpdateStatus)
            self.botThread.start()
            self.statusLabel.setText("🟢 الحالة: شغال يحبيب اخوك")

    def stopBot(self):
        if self.botThread and self.botThread.isRunning():
            self.botThread.stop()
            self.botThread.quit()
            self.botThread.wait()
            self.statusLabel.setText("⚪ الحالة: متوقف")

    def onUpdateStatus(self, msg):
        print(msg)
        self.statusLabel.setText(f"🟠 {msg}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    def global_stop():
        if window.botThread and window.botThread.isRunning():
            window.stopBot()

    keyboard.on_press_key('ctrl', lambda _: global_stop())
    sys.exit(app.exec_())
