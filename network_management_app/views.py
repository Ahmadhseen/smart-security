from django.shortcuts import render, redirect
from django.db.models import Count
from network_management_app.forms import AntennaForm, EditAntennaForm, TowerForm
from .models import Antenna, Tower
from django.contrib import messages

# Create your views here.
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
        form = EditAntennaForm(request.POST, instance=antenna)
        if form.is_valid():
            form.save()
            messages.success(request, f'Antenna {antenna.name_device} updated successfully.')
        return redirect('dashboard')
    else:
        form = EditAntennaForm(instance=antenna)

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