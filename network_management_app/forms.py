from django import forms
from .models import Users

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