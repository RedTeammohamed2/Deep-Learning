import sys
import time
import pyautogui
import keyboard  # مكتبة لتسجيل اختصارات عالمية
from PyQt5 import QtWidgets, QtCore, QtGui

# ثريد لتنفيذ النقر التلقائي
class ClickWorker(QtCore.QThread):
    update_status = QtCore.pyqtSignal(str)

    def __init__(self, delay, iterations=None):
        """
        :param delay: التأخير بين النقرات (بالثواني)
        :param iterations: عدد النقرات المطلوب تنفيذها، None يعني تكرار غير محدود
        """
        super().__init__()
        self.delay = delay
        self.iterations = iterations  # None يعني غير محدود
        self._running = True

    def run(self):
        self.update_status.emit("البوت شغال... 🚀")
        count = 0
        if self.iterations is None:  # تكرار غير محدود
            while self._running:
                pyautogui.click()
                count += 1
                self.update_status.emit(f"عدد النقرات: {count}")
                time.sleep(self.delay)
        else:
            while self._running and count < self.iterations:
                pyautogui.click()
                count += 1
                self.update_status.emit(f"عدد النقرات: {count}")
                time.sleep(self.delay)
            self._running = False  # انتهى عدد النقرات المحدد
        self.update_status.emit("البوت توقف. 😢")

    def stop(self):
        self._running = False

# النافذة الرئيسية بستايل مستقبل 2025
class MainWindow(QtWidgets.QMainWindow):
    globalToggle = QtCore.pyqtSignal()  # إشارة للتبديل العالمي

    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()
        # ربط الإشارة مع دالة التبديل
        self.globalToggle.connect(self.toggle_bot)
        # تسجيل اختصار Ctrl كاختصار عالمي (سيعمل حتى لو النافذة في الخلفية)
        keyboard.add_hotkey('ctrl', lambda: self.globalToggle.emit())

    def init_ui(self):
        self.setWindowTitle("بوت النقر التلقائي - مستقبل 2025")
        self.resize(500, 350)
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        # ستايل عام للواجهة
        style = """
        QWidget {
            background-color: #0d0d0d;
            color: #e0e0e0;
            font-family: 'Segoe UI', sans-serif;
            font-size: 15px;
        }
        QDoubleSpinBox, QSpinBox, QComboBox {
            background-color: #1e1e1e;
            border: 1px solid #444;
            border-radius: 5px;
            padding: 5px;
            color: #e0e0e0;
        }
        QPushButton {
            background-color: #00acc1;
            border: none;
            color: #fff;
            border-radius: 5px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #26c6da;
        }
        QLabel {
            font-size: 16px;
        }
        """
        self.setStyleSheet(style)

        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        form_layout = QtWidgets.QFormLayout()
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)

        # حقل إدخال قيمة التأخير باستخدام QDoubleSpinBox
        self.delay_label = QtWidgets.QLabel("التأخير:")
        self.delay_spin = QtWidgets.QDoubleSpinBox()
        self.delay_spin.setRange(0.001, 3600)
        self.delay_spin.setDecimals(3)
        self.delay_spin.setValue(1.0)
        form_layout.addRow(self.delay_label, self.delay_spin)

        # قائمة اختيار لوحدة التأخير
        self.unit_label = QtWidgets.QLabel("الوحدة:")
        self.unit_combo = QtWidgets.QComboBox()
        self.unit_combo.addItems(["مللي ثانية", "ثانية", "دقيقة", "ساعة"])
        form_layout.addRow(self.unit_label, self.unit_combo)

        # حقل إدخال عدد التكرارات باستخدام QSpinBox
        self.iterations_label = QtWidgets.QLabel("عدد التكرارات:")
        self.iterations_spin = QtWidgets.QSpinBox()
        self.iterations_spin.setRange(1, 1000000)
        self.iterations_spin.setValue(10)
        form_layout.addRow(self.iterations_label, self.iterations_spin)

        # خانة اختيار "تكرار غير محدود" مع تصميم تبديل حديث
        self.infinite_checkbox = QtWidgets.QCheckBox("تكرار غير محدود")
        # تحسين شكل المفتاح باستخدام StyleSheet ليظهر كمفتاح تبديل (Toggle Switch)
        self.infinite_checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 10px;
                font-size: 15px;
            }
            QCheckBox::indicator {
                width: 60px;
                height: 30px;
                border-radius: 15px;
                background-color: #555;
                transition: background-color 0.3s ease;
            }
            QCheckBox::indicator:checked {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00acc1, stop:1 #26c6da);
            }
            QCheckBox::indicator:unchecked:hover {
                background-color: #666;
            }
            QCheckBox::indicator:checked:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #26c6da, stop:1 #00acc1);
            }
        """)
        form_layout.addRow("", self.infinite_checkbox)
        # ربط تغيير حالة خانة الاختيار بتعطيل/تمكين حقل عدد التكرارات
        self.infinite_checkbox.toggled.connect(self.toggle_iterations_spin)

        layout.addLayout(form_layout)

        # تسمية الحالة
        self.status_label = QtWidgets.QLabel("الحالة: انتظار...")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # تعليمات الاستخدام
        instructions = QtWidgets.QLabel("اضغط على مفتاح Ctrl لتبديل التشغيل/الإيقاف (اختصار عالمي).")
        instructions.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(instructions)

        # ضبط التركيز لالتقاط ضغطات المفاتيح
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()

    def toggle_iterations_spin(self, checked):
        # تعطيل حقل عدد التكرارات إذا كان خيار التكرار غير المحدود مفعل
        self.iterations_spin.setEnabled(not checked)

    def toggle_bot(self):
        if self.worker is None or not self.worker.isRunning():
            self.start_bot()
        else:
            self.stop_bot()

    def start_bot(self):
        base_value = self.delay_spin.value()
        unit = self.unit_combo.currentText()
        if unit == "مللي ثانية":
            delay = base_value / 1000.0
        elif unit == "ثانية":
            delay = base_value
        elif unit == "دقيقة":
            delay = base_value * 60
        elif unit == "ساعة":
            delay = base_value * 3600
        else:
            delay = base_value

        if self.infinite_checkbox.isChecked():
            iterations = None
        else:
            iterations = self.iterations_spin.value()

        if self.worker is None or not self.worker.isRunning():
            self.worker = ClickWorker(delay, iterations)
            self.worker.update_status.connect(self.update_status)
            self.worker.start()
            self.status_label.setText("البوت شغال... 🚀")
        else:
            self.status_label.setText("البوت شغال بالفعل! ⚠️")

    def stop_bot(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
            self.status_label.setText("البوت توقف. 😢")
        else:
            self.status_label.setText("البوت مش شغال! ⚠️")

    def update_status(self, msg):
        self.status_label.setText(msg)

    def closeEvent(self, event):
        keyboard.clear_all_hotkeys()
        event.accept()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
