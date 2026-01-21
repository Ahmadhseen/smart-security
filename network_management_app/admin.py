from django.contrib import admin
from .models import Antenna, Tower
# Register your models here.

admin.site.site_header = "smart security Admin"

class AntennaAdmin(admin.ModelAdmin):
    list_display = ('name_device', 'model_device', 'ip_address', 'encreption_type', 'frequency', 'tower')
    search_fields = ('name_device', 'model_device', 'ip_address')
    list_filter = ('encreption_type', 'frequency')

admin.site.register(Antenna, AntennaAdmin)

class TowerAdmin(admin.ModelAdmin):
    list_display = ('name_tower', 'location', 'height')
    search_fields = ('name_tower', 'location')
    list_filter = ('height',)

admin.site.register(Tower, TowerAdmin)