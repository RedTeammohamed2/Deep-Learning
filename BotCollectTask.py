import customtkinter as ctk
import pyautogui
import time
import keyboard
import threading
from datetime import datetime

class AllianceBot:
    def __init__(self):
        self.running = False
        self.main_image = "button.png"
        self.secondary_images = ["button1.png", "button2.png"]
        self.attempts = 0
        self.speed = 1  # السرعة الافتراضية (1 ثانية)
        
    def find_and_click(self):
        while self.running:
            try:
                if self.attempts < 5:
                    self.search_main_image()
                else:
                    # الانتظار 3 ثواني قبل البحث عن الصور الثانوية
                    print("انتظار 1 ثواني قبل البحث عن البدائل...")
                    self.update_status("انتظار 1 ثواني قبل البحث عن البدائل...")
                    time.sleep(1)
                    self.search_secondary_images()
                    self.attempts = 0  # إعادة تعيين المحاولات بعد البحث الثانوي
            except Exception as e:
                print(f"خطأ: {str(e)}")
                time.sleep(self.speed)

    def search_main_image(self):
        try:
            print(f"البحث عن الصورة الرئيسية... المحاولة {self.attempts + 1}/11")
            template = pyautogui.locateOnScreen(
                self.main_image,
                confidence=0.8,  # الدقة 0.9
                grayscale=True
            )
            if template:
                print("تم العثور على الصورة الرئيسية!")
                self.click_image(template, "الصورة الرئيسية")
                self.attempts = 0  # إعادة تعيين المحاولات عند النجاح
            else:
                self.attempts += 1
                print(f"لم يتم العثور على الصورة الرئيسية. المحاولة {self.attempts}/11")
                self.update_status(f"جاري البحث... {self.attempts}/11")
                
            self.update_progress()
            time.sleep(self.speed)  # استخدام السرعة المحددة
            
        except Exception as e:
            print(f"خطأ في البحث عن الصورة الرئيسية: {str(e)}")
            self.attempts += 1  # زيادة العداد في حالة حدوث خطأ

    def search_secondary_images(self):
        try:
            print("بدء البحث عن الصور الثانوية...")
            self.update_status("جاري البحث عن البدائل...")
            clicked_any = False
            
            for image in self.secondary_images:
                if not self.running:
                    break  # توقف إذا تم إيقاف البوت
                    
                print(f"البحث عن الصورة الثانوية: {image}")
                template = pyautogui.locateOnScreen(
                    image,
                    confidence=0.9,  # الدقة 0.9
                    grayscale=True
                )
                if template:
                    print(f"تم العثور على الصورة الثانوية: {image}")
                    self.click_image(template, f"الصورة الثانوية {image}")
                    clicked_any = True
                    time.sleep(1)  # انتظر ثانية بين كل محاولة ثانوية
                    
            if not clicked_any:
                print("لم يتم العثور على أي صور ثانوية")
                self.update_status("لم يتم العثور على بدائل")
            
            self.update_progress()
            
        except Exception as e:
            print(f"خطأ في البحث الثانوي: {str(e)}")

    def click_image(self, template, image_name):
        try:
            center_x = template.left + template.width // 2
            center_y = template.top + template.height // 2
            pyautogui.click(center_x, center_y)
            print(f"تم النقر بنجاح على {image_name}")
            self.update_status(f"تم الضغط على {image_name}")
            time.sleep(self.speed)  # استخدام السرعة المحددة
        except Exception as e:
            print(f"فشل النقر على {image_name}: {str(e)}")

    def start(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.find_and_click, daemon=True).start()
            print("تم تشغيل البوت")
            self.update_status("الحالة: نشط")

    def stop(self):
        self.running = False
        print("تم إيقاف البوت")
        self.update_status("الحالة: متوقف")
        self.attempts = 0
        self.update_progress()

    def set_speed(self, speed):
        self.speed = speed
        print(f"تم تغيير السرعة إلى {speed} ثانية")

    def update_status(self, message):
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=message)

    def update_progress(self):
        if hasattr(self, 'progress_bar'):
            progress = min((self.attempts / 11) * 100, 100)
            self.progress_bar.set(progress / 100)

# تعريف الواجهة
class ModernGUI:
    def __init__(self):
        self.bot = AllianceBot()
        self.setup_gui()

    def setup_gui(self):
        # تعيين المظهر العام
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # إنشاء النافذة الرئيسية
        self.root = ctk.CTk()
        self.root.title("بوت مهام التحالف 2025")
        self.root.geometry("600x700")

        # إطار رئيسي
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # العنوان
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="بوت مهام التحالف 2025",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=20)

        # إطار الحالة
        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.pack(padx=20, pady=10, fill="x")

        self.bot.status_label = ctk.CTkLabel(
            self.status_frame,
            text="الحالة: متوقف",
            font=ctk.CTkFont(size=16)
        )
        self.bot.status_label.pack(pady=10)

        # شريط التقدم
        self.bot.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.bot.progress_bar.pack(padx=20, pady=10, fill="x")
        self.bot.progress_bar.set(0)

        # إطار الأزرار
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(padx=20, pady=20, fill="x")

        # زر التشغيل
        self.start_button = ctk.CTkButton(
            self.button_frame,
            text="تشغيل البوت",
            command=self.start_bot,
            font=ctk.CTkFont(size=16),
            height=50
        )
        self.start_button.pack(pady=10, fill="x")

        # زر الإيقاف
        self.stop_button = ctk.CTkButton(
            self.button_frame,
            text="إيقاف البوت",
            command=self.stop_bot,
            font=ctk.CTkFont(size=16),
            height=50,
            fg_color="#FF5252",
            hover_color="#FF1744"
        )
        self.stop_button.pack(pady=10, fill="x")

        # إطار السرعة
        self.speed_frame = ctk.CTkFrame(self.main_frame)
        self.speed_frame.pack(padx=20, pady=10, fill="x")

        # قائمة السرعة
        self.speed_label = ctk.CTkLabel(
            self.speed_frame,
            text="اختر سرعة البوت:",
            font=ctk.CTkFont(size=14)
        )
        self.speed_label.pack(side="left", padx=10)

        self.speed_menu = ctk.CTkOptionMenu(
            self.speed_frame,
            values=["0.001 ثانية", "1 ثانية", "5 ثواني", "10 ثواني"],
            command=self.change_speed
        )
        self.speed_menu.pack(side="left", padx=10)
        self.speed_menu.set("1 ثانية")  # القيمة الافتراضية

        # إطار المعلومات
        self.info_frame = ctk.CTkFrame(self.main_frame)
        self.info_frame.pack(padx=20, pady=10, fill="x")

        # معلومات الاختصارات
        self.shortcut_label = ctk.CTkLabel(
            self.info_frame,
            text="⌨️ اضغط Ctrl + Q لإيقاف البوت",
            font=ctk.CTkFont(size=14)
        )
        self.shortcut_label.pack(pady=10)

        # تبديل المظهر
        self.appearance_menu = ctk.CTkOptionMenu(
            self.main_frame,
            values=["Dark", "Light", "System"],
            command=self.change_appearance
        )
        self.appearance_menu.pack(pady=10)

        # إعداد الاختصارات
        self.setup_hotkeys()

    def change_appearance(self, new_appearance):
        ctk.set_appearance_mode(new_appearance.lower())

    def change_speed(self, speed):
        if speed == "0.001 ثانية":
            self.bot.set_speed(0.001)
        elif speed == "1 ثانية":
            self.bot.set_speed(1)
        elif speed == "5 ثواني":
            self.bot.set_speed(5)
        elif speed == "10 ثواني":
            self.bot.set_speed(10)

    def setup_hotkeys(self):
        keyboard.add_hotkey('ctrl+q', self.stop_bot)

    def start_bot(self):
        self.bot.start()
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
    def stop_bot(self):
        self.bot.stop()
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.bot.progress_bar.set(0)

    def run(self):
        self.root.mainloop()

# تشغيل البرنامج
if __name__ == "__main__":
    gui = ModernGUI()
    gui.run()