from django import forms
from .models import Antenna, Tower, Users

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

class TowerForm(forms.ModelForm):
    class Meta:
        model = Tower
        fields = '__all__'
        widgets = {
            'name_tower': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class UsersForm(forms.ModelForm):
        class Meta:
            model = Users
            fields = '__all__'
            widgets = {
                'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                'password': forms.PasswordInput(attrs={'class': 'form-control'}),
                'username': forms.TextInput(attrs={'class': 'form-control'}),
            }

class LogInForm(forms.Form):
        username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
        password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))