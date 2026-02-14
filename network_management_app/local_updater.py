import requests
import time
from .ssh_services import get_antenna_live_data
from .models import Antenna

API_URL = "https://smartsecurity.pythonanywhere.com/api/sync-antenna/"
HEADERS = {"X-Api-Key": "smartsecurity"}

def update_all_live():
    # نجلب الصحون من قاعدة بيانات المكتب
    antennas = Antenna.objects.all()
    for ant in antennas:
        data = get_antenna_live_data(ant.ip_address, 'ubnt', ant.password)
        if data['status'] == 'Online':
            payload = {
                "action": "save",
                "data": {
                    "ip_address": ant.ip_address,
                    "signal": data['signal'],
                    "ccq": data['ccq'],
                    "status": "Online",
                    "number_of_clients": data['number_of_clients']
                }
            }
            requests.post(API_URL, json=payload, headers=HEADERS)

while True:
    update_all_live()
    time.sleep(300) # تحديث كل 5 دقائق