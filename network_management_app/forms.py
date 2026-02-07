from django import forms
from .models import Antenna, Tower, Users

class AntennaForm(forms.ModelForm):
    class Meta:
        model = Antenna
        fields = ['ip_address', 'password', 'tower'] 
        widgets = {
            'ip_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '192.168.1.20'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'tower': forms.Select(attrs={'class': 'form-control'}),
        }
        

class TowerForm(forms.ModelForm):
    class Meta:
        model = Tower
        fields = '__all__'
        widgets = {
            'name_tower': forms.TextInput(attrs={'class': 'form-control'}),
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