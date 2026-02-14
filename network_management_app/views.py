from django.shortcuts import render, redirect
from django.db.models import Count
from .forms import UsersForm, LogInForm
from .models import Antenna, Tower, Users
from django.contrib import messages
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def dashboard(request):
    towers = Tower.objects.all()
    tower_id = request.GET.get('tower_filter')
    if tower_id:
        antennas = Antenna.objects.filter(tower__id=tower_id)
    else: 
        antennas = Antenna.objects.all()
    return render(request, 'network_management_app/dashboard.html', {'antennas': antennas, 'towers': towers})
       

def view_towers(request):
    towers = Tower.objects.annotate(num_antennas=Count('antennas'))
    return render(request, 'network_management_app/view_towers.html', {'towers': towers})

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


    

MY_SECRET_KEY = "smartsecurity1234"

@csrf_exempt
def sync_antenna_api(request):
    auth_key = request.headers.get('X-Api-Key')
    if auth_key != MY_SECRET_KEY:
        return JsonResponse({"status": "unauthorized"}, status=401)

    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            action = payload.get('action') # 'save' أو 'delete'
            data = payload.get('data')

            if action == 'save':
                tower_name = data.get('tower_name')
                tower_obj = None
                if tower_name:
                    # ابحث عن البرج بالاسم، وإذا لم تجده أنشئه
                    tower_obj, _ = Tower.objects.get_or_create(name_tower=tower_name)

                # تحديث إذا كان موجوداً، أو إنشاء واحد جديد
                antenna, created = Antenna.objects.update_or_create(
                    ip_address=data['ip_address'],
                    defaults={
                        'name_device': data.get('name_device'),
                        'model_device': data.get('model_device'),
                        'operation_mode': data.get('operation_mode'),
                        'signal': data.get('signal'),
                        'noise': data.get('noise'),
                        'ccq': data.get('ccq'),
                        'number_of_clients': data.get('number_of_clients', 0),
                        'status': data.get('status'),
                        'essid': data.get('essid'),
                        'password': data.get('password'),
                        'tower': tower_obj,
                    }
                )
                return JsonResponse({"status": "success", "action": "saved"})

            elif action == 'delete':
                Antenna.objects.filter(ip_address=data['ip_address']).delete()
                return JsonResponse({"status": "success", "action": "deleted"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "failed"}, status=405)