from django.contrib import admin
from .models import Antenna, Tower, Users
# Register your models here.

admin.site.site_header = "smart security Admin"

class AntennaAdmin(admin.ModelAdmin):
    list_display = ('name_device', 'model_device', 'ip_address', 'encryption', 'frequency', 'tower')
    search_fields = ('name_device', 'model_device', 'ip_address')
    list_filter = ('encryption', 'frequency')

admin.site.register(Antenna, AntennaAdmin)

class TowerAdmin(admin.ModelAdmin):
    list_display = ['name_tower']

admin.site.register(Tower, TowerAdmin)

class UsersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'password', 'username')
    search_fields = ('first_name', 'last_name', 'username')
    list_filter = ('first_name', 'last_name', 'username')
admin.site.register(Users, UsersAdmin)