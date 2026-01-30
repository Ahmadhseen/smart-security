import paramiko
import re

def get_antenna_live_data(ip, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
       
        ssh.connect(
            ip, username=username, password=password, 
            disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']},
            timeout=5
        )

     
        stdin, stdout, stderr = ssh.exec_command('mca-status')
        status_out = stdout.read().decode()
        
        stdin, stdout, stderr = ssh.exec_command('cat /tmp/system.cfg')
        config_out = stdout.read().decode()
        ssh.close()

        def extract(key, text):
            pattern = fr'{key}=([^,\n\r]+)'
            match = re.search(pattern, text)
            return match[1].strip() if match else "N/A"
        
        wpa_mode = extract(r'aaa\.1\.wpa\.mode', config_out)
        encryption = "WPA2-AES" if wpa_mode == "2" else "WPA-AES" if wpa_mode == "1" else "Open"

        raw_ccq = extract('ccq', status_out)
        ccq_final = f"{int(raw_ccq)/10}%" if raw_ccq.isdigit() else "0%" 

        op_mode = extract('wlanOpmode', status_out)
        mode_desc = "Access Point" if op_mode in ["ap", "ap-ptp-ac", "ap-ptmp-mixed"] else "Station"

        return {
            "device_name": extract('deviceName', status_out),
            "platform": extract('platform', status_out),
            "operation_mode": mode_desc,
            "signal": f"{extract('signal', status_out)} dBm",
            "noise": f"{extract('noise', status_out)} dBm",
            "ccq": ccq_final,
            "lan_speed": extract('lanSpeed', status_out),
            "number_of_clients": extract('wlanConnections', status_out),
            "uptime_hours": f"{int(extract('uptime', status_out)) // 3600} hours",
            "essid": extract('essid', status_out),
            "frequency": f"{extract('freq', status_out)} MHz",
            "channel_width": f"{extract('chanbw', status_out)} MHz",
            "distance": f"{extract('distance', status_out)} m",
            "encryption": encryption,
            "psk": extract(r'aaa\.1\.wpa\.psk', config_out),
            "status": "Online"
        }
    except Exception as e:
        return {"status": "Offline", "error": str(e)}