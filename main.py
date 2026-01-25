import webview
import threading
import os
import sys
import time
from django.core.management import execute_from_command_line

def resource_path(relative_path):
    """ دالة لجلب المسار الصحيح للملفات سواء كنت بتشغل الكود عادي أو كملف EXE """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# الآن لما تستدعي أي ملف (أيقونة أو غيره) استخدم الدالة:
icon_path = resource_path('icon.ico')

# 1. دالة لتشغيل سيرفر Django في الخلفية
def run_django():
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings') # استبدل your_project_name باسم مجلد إعداداتك
    execute_from_command_line(['manage.py', 'runserver', '--noreload'])

if __name__ == '__main__':
    # 2. تشغيل السيرفر في Thread منفصل حتى لا يتوقف البرنامج
    t = threading.Thread(target=run_django)
    t.daemon = True
    t.start()

    # 2. انتظر لمدة 3 إلى 5 ثوانٍ ليعطي Django وقتاً للإقلاع
    time.sleep(5)

    # 3. فتح نافذة البرنامج وعرض رابط السيرفر المحلي
    webview.create_window('Smart Security', 'http://127.0.0.1:8000', maximized=True)
    webview.start(icon=icon_path)