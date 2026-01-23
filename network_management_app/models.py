from django.db import models

# Create your models here.

class Antenna(models.Model):
    name_device = models.CharField(max_length=100)
    model_device = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    encreption_type = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    frequency = models.CharField(max_length=50)
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
    