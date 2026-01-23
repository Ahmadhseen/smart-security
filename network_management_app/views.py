from django.shortcuts import render, redirect
from django.db.models import Count
from network_management_app.forms import AntennaForm, TowerForm, UsersForm, LogInForm
from .models import Antenna, Tower, Users
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'network_management_app/home.html')

def dashboard(request):
    towers = Tower.objects.all()
    if towers_id:= request.GET.get('tower_filter'):
        antennas = Antenna.objects.filter(tower__id=towers_id)

    else: 
        antennas = Antenna.objects.all()
    context = {
        'antennas': antennas,
        'towers': towers
    }
    return render(request, 'network_management_app/dashboard.html', context)


def add(request):
    if request.POST:
        form = AntennaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Antenna added successfully.')
            return redirect('dashboard')
    else:
        form = AntennaForm()
    messages.info(request, 'Please fill out the form to add a new antenna.')
    # إذا كنت تريد تمرير الأبراج يدوياً لاستخدامها في HTML مخصص:
    towers = Tower.objects.all() 
    return render(request, 'network_management_app/add.html', {'form': form, 'towers': towers})

def edit(request, pk):
    antenna = Antenna.objects.get(pk=pk)
    if request.POST:
        form = AntennaForm(request.POST, instance=antenna)
        if form.is_valid():
            form.save()
            messages.success(request, f'Antenna {antenna.name_device} updated successfully.')
        return redirect('dashboard')
    else:
        form = AntennaForm(instance=antenna)

    return render(request, 'network_management_app/edit.html', {'antenna':antenna, 'form': form})

def delete(request, pk):
    antenna = Antenna.objects.get(pk=pk)
    antenna.delete()
    messages.success(request, f'Antenna {antenna.name_device} deleted successfully.')
    return redirect('dashboard')

def add_tower(request):
    if request.POST:
        form = TowerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tower added successfully.')
            return redirect('view_towers')
    else:
        form = TowerForm()
    return render(request, 'network_management_app/add_tower.html', {'form': form})
       

def view_towers(request):
    towers = Tower.objects.annotate(num_antennas=Count('antennas'))
    return render(request, 'network_management_app/view_towers.html', {'towers': towers})

def delete_tower(request, pk):
    tower = Tower.objects.get(pk=pk)
    tower.delete()
    messages.success(request, f'Tower {tower.name} deleted successfully.')
    return redirect('view_towers')

def edit_tower(request, pk):
    tower = Tower.objects.get(pk=pk)
    if request.POST:
        form = TowerForm(request.POST, instance=tower)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tower {tower.name} updated successfully.')
            return redirect('view_towers')
    else:
        form = TowerForm(instance=tower)
    return render(request, 'network_management_app/edit_tower.html', {'form': form, 'tower': tower})

def sign_in(request):
    if request.POST:
        form = UsersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sign in successful.')
            return redirect('log_in')
    else:
        form = UsersForm()    
    return render(request, 'network_management_app/sign_in.html', {'form': form})

def log_in(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = Users.objects.get(username=username, password=password)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        except Users.DoesNotExist:
            messages.error(request, 'Invalid username or password. Please try again.')
    
    form = LogInForm()
    return render(request, 'network_management_app/log_in.html', {'form': form})