import paramiko
import re

def get_antenna_selected_info(ip, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            ip, 
            username=username, 
            password=password, 
            disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']},
            timeout=10
        )

        # تنفيذ الأوامر وجلب المخرجات
        stdin, stdout, stderr = ssh.exec_command('mca-status')
        status_out = stdout.read().decode()
        
        stdin, stdout, stderr = ssh.exec_command('cat /tmp/system.cfg')
        config_out = stdout.read().decode()
        ssh.close()

        # دالة البحث عن القيم
        def extract(key, text):
            pattern = fr'{key}=([^,\n\r]+)'
            match = re.search(pattern, text)
            return match[1].strip() if match else "N/A"

        # --- معالجة البيانات المختارة ---
        
        # 1. تحديد نوع التشفير (بناءً على ملفك: mode=1 تعني WPA)
        wpa_mode = extract(r'aaa\.1\.wpa\.mode', config_out)
        encryption = "WPA2-AES" if wpa_mode == "2" else "WPA-AES" if wpa_mode == "1" else "Open"

        # 2. جودة الإشارة CCQ
        raw_ccq = extract('ccq', status_out)
        ccq_final = f"{int(raw_ccq)/10}%" if raw_ccq.isdigit() else "0%"

        # 3. وضع التشغيل
        op_mode = extract('wlanOpmode', status_out)
        mode_desc = "مرسل (Access Point)" if op_mode == "ap" else "مستقبل (Station)"

        # تجميع المعلومات المطلوبة فقط
        results = {
            "اسم الجهاز": extract('deviceName', status_out),
            "النوع (Platform)": extract('platform', status_out),
            "وضع التشغيل": mode_desc,
            "قوة الإشارة": f"{extract('signal', status_out)} dBm",
            "مستوى الضجيج": f"{extract('noise', status_out)} dBm",
            "الجودة (CCQ)": ccq_final,
            "سرعة (LAN)": extract('lanSpeed', status_out),
            "عدد المتصلين": extract('wlanConnections', status_out),
            "مدة التشغيل": f"{int(extract('uptime', status_out)) // 3600} ساعة",
            "اسم الشبكة (ESSID)": extract('essid', status_out),
            "التردد": f"{extract('freq', status_out)} MHz",
            "عرض الموجة": f"{extract('chanbw', status_out)} MHz",
            "المسافة": f"{extract('distance', status_out)} متر",
            "نوع التشفير": encryption,
            "كلمة سر الربط": extract(r'aaa\.1\.wpa\.psk', config_out)
        }

        return results

    except Exception as e:
        return {"error": str(e)}

# الطباعة بشكل جميل
info = get_antenna_selected_info('192.168.50.26', 'ubnt', 'smart2025')

if "error" not in info:
    print("\n" + "═"*45)
    print(f"📡 تقرير البيانات المختارة - {info['اسم الجهاز']}")
    print("═"*45)
    for key, value in info.items():
        print(f"║ {key: <20}: {value}")
    print("═"*45)
else:
    print(f"❌ حدث خطأ: {info['error']}")