from django import forms
from .models import Antenna, Tower

class AntennaForm(forms.ModelForm):
    class Meta:
        model = Antenna
        fields = '__all__'
        widgets = {
            'name_device': forms.TextInput(attrs={'class': 'form-control'}),
            'model_device': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
            'encreption_type': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'frequency': forms.NumberInput(attrs={'class': 'form-control'}),
            'tower': forms.Select(attrs={'class': 'form-control'}),
        }
        # 'tower' هو اسم الحقل الذي يربط الهوائي بالبرج في الموديل

class EditAntennaForm(forms.ModelForm):
    class Meta:
        model = Antenna
        fields = '__all__'
        widgets = {
            'name_device': forms.TextInput(attrs={'class': 'form-control'}),
            'model_device': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
            'encreption_type': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'frequency': forms.NumberInput(attrs={'class': 'form-control'}),
            'tower': forms.Select(attrs={'class': 'form-control'}),
        }


class TowerForm(forms.ModelForm):
    class Meta:
        model = Tower
        fields = '__all__'
        widgets = {
            'name_tower': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
        }