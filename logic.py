# logic.py
import sys
import os
import time
import threading
import subprocess
import pyautogui
import keyboard
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

# متغير للتحكم في حالة تشغيل البوت
stop_event = threading.Event()

# دالة إيقاف البوت عند الضغط على Ctrl + Q
def stop_bot():
    stop_event.set()  # تغيير حالة الـ Event لإيقاف العمليات
    print("تم الضغط على Ctrl + Q. جاري إيقاف البوت...")

# تشغيل خاصية إيقاف البوت في خلفية البرنامج
keyboard_thread = threading.Thread(target=lambda: keyboard.add_hotkey('ctrl+q', stop_bot), daemon=True)
keyboard_thread.start()

def نقل_الموارد_بالترتيب_وتكرار(سرعة):
    stop_event.clear()  # إعادة تعيين الـ Event عند بدء التشغيل

    # إنشاء نافذة جديدة لاختيار عدد التكرارات
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
    repeat_window = QWidget()
    repeat_window.setWindowTitle("اختيار عدد التكرارات")
    repeat_window.setGeometry(100, 100, 400, 300)
    repeat_window.setStyleSheet("""
        background-color: #1e1e2f;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    """)

    layout = QVBoxLayout()

    # تسمية تعليمات للمستخدم
    instruction_label = QLabel("اختر عدد التكرارات أو اضغط على 'لا نهائي' للتكرار بدون توقف:")
    instruction_label.setStyleSheet("""
        font-size: 14px;
        color: #ffffff;
        margin-bottom: 20px;
    """)
    instruction_label.setAlignment(Qt.AlignCenter)
    layout.addWidget(instruction_label)

    # حقل إدخال عدد التكرارات
    repeat_entry = QLineEdit()
    repeat_entry.setPlaceholderText("أدخل عدد التكرارات هنا...")
    repeat_entry.setStyleSheet("""
        font-size: 14px;
        background-color: #2a2a3f;
        color: #ffffff;
        border: 2px solid #4a90e2;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
    """)
    layout.addWidget(repeat_entry)

    # الدالة التي تنفذ عملية التكرار
    def start_repeating(عدد_التكرار):
        try:
            image_paths = [
                os.path.join('images', 'resources_button1.png'),
                os.path.join('images', 'resources_button2.png'),
                os.path.join('images', 'resources_button3.png'),
                os.path.join('images', 'resources_button4.png')
            ]

            i = 0
            while i < عدد_التكرار and not stop_event.is_set():
                print(f"بدء التكرار {i + 1}...")

                for image_path in image_paths:
                    if stop_event.is_set():
                        break

                    print(f"بندور علي الصوره {image_path}")
                    region = (0, 0, 1920, 1080)  # تحديد المنطقة التي سيتم البحث فيها

                    for attempt in range(5):
                        if stop_event.is_set():
                            break

                        try:
                            button_location = pyautogui.locateOnScreen(
                                image_path, region=region, confidence=0.9
                            )
                            if button_location:
                                center_x, center_y = pyautogui.center(button_location)
                                pyautogui.click(center_x, center_y)
                                print(f"تم النقر على الصورة: {image_path}")
                                break
                            else:
                                print(f"لم يتم العثور على الصورة: {image_path} (محاولة {attempt + 1})")
                                time.sleep(0.5)
                        except Exception as e:
                            print(f"في مشكله يسطا {image_path}: {str(e)}")
                    else:
                        print(f"فشل العثور على الصورة {image_path} بعد 5 محاولات. تم تخطيها.")

                print(f"تم الانتهاء من التكرار {i + 1}")
                i += 1

            if عدد_التكرار != float('inf') and not stop_event.is_set():
                print(f"تم تنفيذ العملية {عدد_التكرار} مرات بنجاح!")
        except Exception as e:
            print(f"حدث خطأ: {str(e)}")
            QMessageBox.critical(repeat_window, "خطأ", f"حدث خطأ أثناء تنفيذ الأوامر: {str(e)}")

    def set_infinite():
        repeat_window.close()
        start_repeating(float('inf'))

    def set_repeat():
        try:
            value = int(repeat_entry.text())
            if value <= 0:
                raise ValueError
            repeat_window.close()
            start_repeating(value)
        except ValueError:
            QMessageBox.critical(repeat_window, "خطأ", "يرجى إدخال عدد صحيح أكبر من 0.")

    # زر "لا نهائي"
    infinite_button = QPushButton("لا نهائي")
    infinite_button.setStyleSheet("""
        background-color: #4a90e2;
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 20px;
        padding: 15px;
        border: none;
        margin-bottom: 10px;
    """)
    infinite_button.clicked.connect(set_infinite)
    layout.addWidget(infinite_button)

    # زر "موافق"
    ok_button = QPushButton("موافق")
    ok_button.setStyleSheet("""
        background-color: #34c759;
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 20px;
        padding: 15px;
        border: none;
        margin-bottom: 10px;
    """)
    ok_button.clicked.connect(set_repeat)
    layout.addWidget(ok_button)

    repeat_window.setLayout(layout)
    repeat_window.show()

def بدء_الإسبام(سرعة):
    stop_event.clear()
    try:
        image_paths = [
            os.path.join('images', 'spam_button1.png'),
            os.path.join('images', 'spam_button2.png'),
            os.path.join('images', 'spam_button3.png'),
            os.path.join('images', 'spam_button4.png')
        ]

        while not stop_event.is_set():
            print("جاري البحث عن الصور...")

            for image_path in image_paths:
                if stop_event.is_set():
                    break

                print(f"بندور على الصورة {image_path}")
                region = (0, 0, 1920, 1080)
                attempts = 0
                image_found = False

                while attempts < 5 and not image_found and not stop_event.is_set():
                    try:
                        button_location = pyautogui.locateOnScreen(
                            image_path, region=region, confidence=0.85
                        )
                        if button_location:
                            center_x, center_y = pyautogui.center(button_location)
                            time.sleep(0.2)
                            pyautogui.click(center_x, center_y)
                            print(f"تم النقر على الصورة: {image_path}")
                            image_found = True
                        else:
                            attempts += 1
                            print(f"لم يتم العثور على الصورة: {image_path}, المحاولة رقم {attempts}")
                    except Exception as e:
                        attempts += 1
                        print(f"في مشكله يسطا {image_path}: {str(e)}")
                    time.sleep(0.2)
                
                if not image_found:
                    print(f"في مشكله يسطا: لم يتم العثور على الصورة {image_path} بعد 5 محاولات.")
                    return

            time.sleep(0.2)

    except Exception as e:
        print(f"حدث خطأ: {str(e)}")
        QMessageBox.critical(None, "خطأ", f"حدث خطأ أثناء تنفيذ الأوامر: {str(e)}")

def open_alliance_tasks():
    try:
        file_name = "BotCollectTask.py"
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        subprocess.Popen(["python", file_path])
        print(f"تم فتح ملف مهام التحالف: {file_name}")
    except Exception as e:
        print(f"حدث خطأ أثناء فتح ملف مهام التحالف: {str(e)}")
        QMessageBox.critical(None, "خطأ", f"حدث خطأ أثناء فتح ملف مهام التحالف: {str(e)}")

def open_collect_gift():
    try:
        file_name = "collectgift.py"
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        subprocess.Popen(["python", file_path])
        print(f"تم فتح ملف collectgift.py")
    except Exception as e:
        print(f"حدث خطأ أثناء فتح ملف collectgift.py: {str(e)}")
        QMessageBox.critical(None, "خطأ", f"حدث خطأ أثناء فتح ملف collectgift.py: {str(e)}")
