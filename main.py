import webview
import threading
import os
import sys
import time
from django.core.management import execute_from_command_line

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def run_django():
    # الحصول على مسار المجلد الحالي حيث يوجد ملف manage.py
    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_path)
    
    # تأكد من كتابة اسم المجلد الذي يحتوي settings.py بدلاً من 'your_project_name'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings') 
    
    try:
        # تشغيل السيرفر على المنفذ 80 كما طلبت
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:80', '--noreload'])
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == '__main__':
    # تشغيل السيرفر في الخلفية
    t = threading.Thread(target=run_django)
    t.daemon = True
    t.start()

    # انتظار بسيط
    time.sleep(5)

    # فتح النافذة (استخدمنا الاسم الذي ضبطته في الـ DNS)
    webview.create_window('Smart Security System', 'http://smart.security', maximized=True)
    webview.start()