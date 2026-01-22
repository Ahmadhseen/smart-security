import paramiko

def get_antenna_raw_info(ip, username, password):
    try:
        # إنشاء اتصال SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password, timeout=5)

        # تنفيذ أمر mstatus للحصول على النص الخام
        stdin, stdout, stderr = ssh.exec_command('mstatus')
        
        # قراءة النتيجة بالكامل كـ نص (String)
        raw_output = stdout.read().decode()
        
        ssh.close()
        return raw_output

    except Exception as e:
        return f"خطأ في الاتصال: {str(e)}"

# تجربة الكود (استبدل القيم ببيانات الصحن عندك)
ip_address = '192.168.50.26'
user = 'ubnt'
passw = 'smart2025'

print("--- المعلومات الخام القادمة من الصحن ---")
print(get_antenna_raw_info(ip_address, user, passw))