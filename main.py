import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow
import logic

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # ربط أزرار الواجهة بالدوال الموجودة في logic.py
    window.start_button.clicked.connect(lambda: logic.نقل_الموارد_بالترتيب_وتكرار(float(window.speed_selector.currentText())))
    window.spam_button.clicked.connect(lambda: logic.بدء_الإسبام(float(window.speed_selector.currentText())))
    window.alliance_button.clicked.connect(logic.open_alliance_tasks)
    window.collectgift_button.clicked.connect(logic.open_collect_gift)


    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
