import threading
import time
import pyautogui
import tkinter as tk

# متغير للتحكم في إيقاف البوت
stop_flag = False

def click_images_continuous():
    global stop_flag
    # قائمة الصور المراد البحث عنها
    image_paths = ['image1.png', 'image2.png', 'image3.png', 'image4.png']
    
    # تكرار العملية باستمرار حتى يتم إيقاف البوت
    while not stop_flag:
        for img in image_paths:
            # انتظار الصورة الحالية حتى يتم العثور عليها والنقر عليها
            while not stop_flag:
                try:
                    # البحث عن مركز الصورة على الشاشة مع ضبط معامل الثقة
                    location = pyautogui.locateCenterOnScreen(img, confidence=0.7)
                    if location:
                        print(f"تم العثور على {img} عند الموقع {location}.")
                        # تحريك الماوس بسرعة إلى موقع الصورة (0.01 ثانية)
                        pyautogui.moveTo(location, duration=0.01)
                        pyautogui.click()
                        # بعد النقر على الصورة، نخرج من حلقة الانتظار للصورة الحالية
                        break
                except Exception as e:
                    print(f"حدث خطأ أثناء البحث عن {img}: {e}")
                time.sleep(0.002)
        # تأخير لمدة ثانية واحدة بعد معالجة جميع الصور قبل بدء دورة جديدة
        time.sleep(1)
    print("انتهت العملية.")

def start_bot():
    global stop_flag
    stop_flag = False
    t = threading.Thread(target=click_images_continuous)
    t.start()

def stop_bot():
    global stop_flag
    stop_flag = True
    print("تم إرسال أمر إيقاف البوت.")

# إنشاء واجهة المستخدم باستخدام Tkinter
root = tk.Tk()
root.title("التحكم في البوت")

start_button = tk.Button(root, text="تشغيل البوت", command=start_bot)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="إيقاف البوت", command=stop_bot)
stop_button.pack(pady=10)

root.mainloop()
