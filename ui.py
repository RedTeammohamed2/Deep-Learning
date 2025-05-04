# ui.py
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QFrame, QScrollArea,
    QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,
    QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import Qt, QTimer

# تعريف ثيمات بسيطة (إذا لم يكن لديك module خارجي للثيمات)
class themes:
    dark_stylesheet = "background-color: #000000;"
    light_stylesheet = "background-color: #ffffff;"

# تغيير قيمة current_mode إلى "dark" ليتم إنشاء الواجهة داخل toggle_theme
current_mode = "dark"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # إعدادات النافذة الرئيسية
        self.setWindowTitle("Lords Mobile Bot 2025 Premium")
        self.setFixedSize(500, 800)
        self.setWindowIcon(QIcon("favicon.ico"))
        self.setStyleSheet("""
            QMainWindow { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ffffff, stop:1 #f8f9fa);
            }
            QLabel, QComboBox, QPushButton { 
                font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #0066ff;
                border-radius: 3px;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        # استدعاء toggle_theme لبناء الواجهة كاملةً (وسيتم إنشاء العناصر مثل start_button)
        toggle_theme(self)

# دالة تبديل الثيم وإنشاء واجهة المستخدم
def toggle_theme(window):
    global current_mode
    if current_mode == "light":
        window.setStyleSheet(themes.dark_stylesheet)
        current_mode = "dark"
    else:
        window.setStyleSheet(themes.light_stylesheet)
        current_mode = "light"
        # إنشاء الـ central widget والـ layout الرئيسي
        central_widget = QWidget()
        window.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # رأس الصفحة المحسن
        header_container = QFrame()
        header_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0066ff, stop:1 #0052cc);
                border-radius: 20px;
                padding: 5px;
            }
        """)
        
        # إضافة تأثير الظل
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 102, 255, 80))
        shadow.setOffset(0, 4)
        header_container.setGraphicsEffect(shadow)
        
        header_layout = QVBoxLayout(header_container)
        
        window.header = QLabel("Lords Mobile Bot")
        window.header.setAlignment(Qt.AlignCenter)
        window.header.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #ffffff;
            padding: 20px 20px 5px 20px;
            letter-spacing: 1px;
        """)
        header_layout.addWidget(window.header)
        
        version_label = QLabel("PREMIUM VERSION 2025")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9);
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 2px;
            padding-bottom: 15px;
        """)
        header_layout.addWidget(version_label)
        
        main_layout.addWidget(header_container)

        # إنشاء منطقة المحتوى المحسنة
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 20px;
                border: 1px solid rgba(0, 102, 255, 0.1);
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(25, 25, 25, 25)
        content_layout.setSpacing(20)

        # قسم اختيار سرعة النقر المحسن
        speed_container = QFrame()
        speed_container.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 15px;
                border: 1px solid rgba(0, 102, 255, 0.1);
                padding: 20px;
            }
        """)
        
        # إضافة تأثير ظل خفيف
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 2)
        speed_container.setGraphicsEffect(shadow)
        
        speed_layout = QVBoxLayout(speed_container)
        speed_layout.setSpacing(12)

        window.speed_label = QLabel("اختر سرعة النقر (ثواني):")
        window.speed_label.setStyleSheet("""
            color: #1a1a1a;
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 0.5px;
        """)
        speed_layout.addWidget(window.speed_label)

        window.speed_selector = QComboBox()
        window.speed_selector.addItems(["0.001", "0.5", "1.0", "1.5", "2.0", "2.5", "3.0"])
        window.speed_selector.setCurrentIndex(2)
        window.speed_selector.setStyleSheet("""
            QComboBox {
                background-color: #ffffff;
                color: #1a1a1a;
                font-size: 15px;
                padding: 12px;
                border-radius: 10px;
                border: 2px solid rgba(0, 102, 255, 0.2);
                selection-background-color: #0066ff;
            }
            QComboBox:hover {
                border: 2px solid #0066ff;
                background-color: rgba(0, 102, 255, 0.05);
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 15px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #0066ff;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                border: 2px solid rgba(0, 102, 255, 0.2);
                border-radius: 10px;
                selection-background-color: rgba(0, 102, 255, 0.1);
                selection-color: #0066ff;
            }
        """)
        speed_layout.addWidget(window.speed_selector)
        content_layout.addWidget(speed_container)

        # تصميم الأزرار المحسن
        button_style = """
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {start_color}, stop:1 {end_color});
                color: #ffffff;
                font-size: 16px;
                font-weight: 600;
                padding: 18px;
                border-radius: 12px;
                border: none;
                letter-spacing: 0.5px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {hover_start}, stop:1 {hover_end});
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {pressed_color}, stop:1 {pressed_color});
                padding-top: 19px;
                padding-bottom: 17px;
            }}
        """

        # زر نقل الموارد
        window.start_button = QPushButton("ابدأ نقل الموارد")
        window.start_button.setStyleSheet(button_style.format(
            start_color="#0066ff",
            end_color="#1a75ff",
            hover_start="#1a75ff",
            hover_end="#3385ff",
            pressed_color="#0052cc"
        ))
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 102, 255, 100))
        shadow.setOffset(0, 4)
        window.start_button.setGraphicsEffect(shadow)
        content_layout.addWidget(window.start_button)

        # زر الإسبام
        window.spam_button = QPushButton("ابدأ الإسبام")
        window.spam_button.setStyleSheet(button_style.format(
            start_color="#00b300",
            end_color="#00cc00",
            hover_start="#00cc00",
            hover_end="#00e600",
            pressed_color="#009900"
        ))
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 179, 0, 100))
        shadow.setOffset(0, 4)
        window.spam_button.setGraphicsEffect(shadow)
        content_layout.addWidget(window.spam_button)

        # زر مهام التحالف
        window.alliance_button = QPushButton("فتح مهام التحالف")
        window.alliance_button.setStyleSheet(button_style.format(
            start_color="#ff6600",
            end_color="#ff751a",
            hover_start="#ff751a",
            hover_end="#ff8533",
            pressed_color="#cc5200"
        ))
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(255, 102, 0, 100))
        shadow.setOffset(0, 4)
        window.alliance_button.setGraphicsEffect(shadow)
        content_layout.addWidget(window.alliance_button)

        # زر فتح collectgift.py
        window.collectgift_button = QPushButton("فتح هدايا التحالف")
        window.collectgift_button.setStyleSheet(button_style.format(
           start_color="#8e44ad",
           end_color="#9b59b6",
           hover_start="#9b59b6",
           hover_end="#8e44ad",
           pressed_color="#732d91"
        ))
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(255, 102, 0, 100))
        shadow.setOffset(0, 4)
        window.collectgift_button.setGraphicsEffect(shadow)
        content_layout.addWidget(window.collectgift_button)

        # قسم التعليمات المحسن
        instruction_container = QFrame()
        instruction_container.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 15px;
                border: 1px solid rgba(0, 102, 255, 0.1);
                padding: 20px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 2)
        instruction_container.setGraphicsEffect(shadow)
        
        instruction_layout = QVBoxLayout(instruction_container)

        shortcuts_title = QLabel("اختصارات لوحة المفاتيح")
        shortcuts_title.setStyleSheet("""
            color: #1a1a1a;
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        """)
        instruction_layout.addWidget(shortcuts_title)

        window.instruction_label = QLabel("Ctrl + Q: إيقاف البوت\nCtrl + F2: بدء نقل الموارد")
        window.instruction_label.setAlignment(Qt.AlignCenter)
        window.instruction_label.setStyleSheet("""
            color: #666666;
            font-size: 14px;
            line-height: 1.6;
            letter-spacing: 0.3px;
        """)
        instruction_layout.addWidget(window.instruction_label)
        
        content_layout.addWidget(instruction_container)

        # إضافة منطقة التمرير
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_frame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        main_layout.addWidget(scroll_area)

        # توقيع محسن
        window.footer_label = QLabel("By RedTeam © 2025")
        window.footer_label.setAlignment(Qt.AlignCenter)
        window.footer_label.setStyleSheet("""
            color: #666666;
            font-size: 14px;
            font-weight: 500;
            padding: 10px;
            letter-spacing: 1px;
        """)
        main_layout.addWidget(window.footer_label)
