from django.db import models
import contextlib
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import requests

# Create your models here.

class Antenna(models.Model):
    name_device = models.CharField(max_length=100)
    model_device = models.CharField(max_length=100)
    operation_mode = models.CharField(max_length=50)
    signal = models.CharField(max_length=50)
    noise = models.CharField(max_length=50)
    ccq = models.CharField(max_length=50)
    lan_speed = models.CharField(max_length=50)
    number_of_clients = models.IntegerField(default=0)
    uptime_hours = models.CharField(max_length=50)
    essid = models.CharField(max_length=100)
    frequency = models.CharField(max_length=50)
    channel_width = models.CharField(max_length=50)
    distance = models.CharField(max_length=50)
    encryption = models.CharField(max_length=50)
    psk = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    ip_address = models.GenericIPAddressField()
    password = models.CharField(max_length=100)
    tower = models.ForeignKey('Tower', on_delete=models.CASCADE, related_name='antennas', null=True, blank=True)

    def __str__(self):
        return f"{self.name_device} - {self.id}"

class Tower(models.Model):
    name_tower = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name_tower} - {self.id}"
    

class Users(models.Model):
   first_name = models.CharField(max_length=50)
   last_name = models.CharField(max_length=50)
   password = models.CharField(max_length=100)
   username = models.CharField(max_length=50, unique=True)

   def __str__(self):
        return self.first_name    


API_URL = "https://smartsecurity.pythonanywhere.com/api/update-all/"
HEADERS = {"X-Api-Key": "smartsecurity1234"}

@receiver(post_save, sender=Antenna)
def sync_on_save(sender, instance, **kwargs):
    payload = {
        "action": "save",
        "data": {
            "ip_address": instance.ip_address,
            "name_device": instance.name_device,
            "model_device": instance.model_device,
            "operation_mode": instance.operation_mode,
            "signal": instance.signal,
            "noise": instance.noise,
            "ccq": instance.ccq,
            "number_of_clients": instance.number_of_clients,
            "status": instance.status,
            "essid": instance.essid,
            "password": instance.password,
            "tower_name": instance.tower.name_tower if instance.tower else None,
        }
    }
    with contextlib.suppress(Exception):
        requests.post(API_URL, json=payload, headers=HEADERS, timeout=5)

@receiver(post_delete, sender=Antenna)
def sync_on_delete(sender, instance, **kwargs):
    payload = {
        "action": "delete",
        "data": {"ip_address": instance.ip_address}
    }
    with contextlib.suppress(Exception):
        requests.post(API_URL, json=payload, headers=HEADERS, timeout=5)
    