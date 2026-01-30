from django.db import models

# Create your models here.

class Antenna(models.Model):
    name_device = models.CharField(max_length=100)
    model_device = models.CharField(max_length=100)
    operation_mode = models.CharField(max_length=50)
    signal = models.CharField(max_length=50)
    noise = models.CharField(max_length=50)
    ccq = models.CharField(max_length=50)
    lan_speed = models.CharField(max_length=50)
    number_of_clients = models.IntegerField()
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
    location = models.CharField(max_length=200)
    height = models.FloatField()

    def __str__(self):
        return f"{self.name_tower} - {self.id}"
    

class Users(models.Model):
   first_name = models.CharField(max_length=50)
   last_name = models.CharField(max_length=50)
   password = models.CharField(max_length=100)
   username = models.CharField(max_length=50, unique=True)

   def __str__(self):
        return self.first_name    
    