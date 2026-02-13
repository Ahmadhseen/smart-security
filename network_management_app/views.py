from django.shortcuts import render, redirect
from django.db.models import Count
from .forms import AntennaForm, TowerForm, UsersForm, LogInForm
from .models import Antenna, Tower, Users
from django.contrib import messages
from django.http import JsonResponse
from .ssh_services import get_antenna_live_data 
# Create your views here.

def dashboard(request):
    towers = Tower.objects.all()
    tower_id = request.GET.get('tower_filter')
    if tower_id:
        antennas = Antenna.objects.filter(tower__id=tower_id)
    else: 
        antennas = Antenna.objects.all()
    return render(request, 'network_management_app/dashboard.html', {'antennas': antennas, 'towers': towers})


def add(request):
    if request.method == 'POST':
        form = AntennaForm(request.POST)
        if form.is_valid():
            # حفظ مبدئي للحصول على الكائن بدون تخزينه في قاعدة البيانات فوراً
            antenna = form.save(commit=False)
            
            # جلب البيانات الحية باستخدام IP وكلمة السر المدخلين
            live_data = get_antenna_live_data(antenna.ip_address, 'ubnt', antenna.password)
            
            if live_data.get('status') == 'Online':
                # تعبئة الحقول تلقائياً من الصحن
                antenna.name_device = live_data.get('device_name')
                antenna.model_device = live_data.get('platform')
                antenna.operation_mode = live_data.get('operation_mode')
                antenna.signal = live_data.get('signal')
                antenna.noise = live_data.get('noise')
                antenna.ccq = live_data.get('ccq')
                antenna.lan_speed = live_data.get('lan_speed')
                antenna.number_of_clients = live_data.get('number_of_clients', 0)
                antenna.uptime_hours = live_data.get('uptime_hours')
                antenna.essid = live_data.get('essid')
                antenna.frequency = live_data.get('frequency')
                antenna.channel_width = live_data.get('channel_width')
                antenna.distance = live_data.get('distance')
                antenna.encryption = live_data.get('encryption')
                antenna.psk = live_data.get('psk')
                antenna.status = 'Online'
                antenna.save()
                messages.success(request, 'Antenna added and data fetched successfully.')
            else:
                # إذا فشل الاتصال، نحفظه كـ Offline أو نرفض الإضافة حسب رغبتك
                antenna.status = 'Offline'
                antenna.save()
                messages.warning(request, 'Failed to fetch live data from the antenna.')
            
            return redirect('dashboard')
    else:
        form = AntennaForm()
    return render(request, 'network_management_app/add.html', {'form': form})

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
            return redirect('home')
    else:
        form = UsersForm()    
    return render(request, 'network_management_app/sign_in.html', {'form': form})

def home(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = Users.objects.get(username=username, password=password)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('view_towers')
        except Users.DoesNotExist:
            messages.error(request, 'Invalid username or password. Please try again.')
    
    form = LogInForm()
    return render(request, 'network_management_app/home.html', {'form': form})


def update_antenna_record(antenna, data):
    """
    هذه الدالة هي التي استخرجتها Sourcery (مع إعادة تسمية منطقية)
    لتحديث بيانات الهوائي من القاموس المستلم
    """
    antenna.signal = data.get('signal')
    antenna.ccq = data.get('ccq')
    antenna.number_of_clients = data.get('number_of_clients', 0)
    antenna.status = 'Online'
    antenna.uptime_hours = data.get('uptime_hours')
    antenna.lan_speed = data.get('lan_speed')
    # لاحظ أننا لم نضع antenna.save() هنا لأنها رُفعت للخارج

def antenna_status_api(request, pk):
    try:
        antenna = Antenna.objects.get(pk=pk)
        data = get_antenna_live_data(antenna.ip_address, 'ubnt', antenna.password)

        if data.get('status') == 'Online':
            update_antenna_record(antenna, data)
        else:
            antenna.status = 'Offline'
            antenna.signal = 'N/A dbm'
            antenna.ccq = 'N/A%'
        
        # Hoisting: تم رفع الحفظ خارج الشرط لأنه مطلوب في الحالتين
        antenna.save() 
        return JsonResponse({"status": antenna.status, "signal": antenna.signal, "ccq": antenna.ccq, "number_of_clients": antenna.number_of_clients})
    
    except Antenna.DoesNotExist:
        return JsonResponse({"status": "Error", "error": "Device not found"}, status=404)