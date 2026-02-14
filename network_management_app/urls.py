from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('view_towers/', views.view_towers, name='view_towers'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('api/antenna-status/<int:pk>/', views.antenna_status_api, name='antenna_status_api'),
    path('api/update-all/', views.sync_antenna_api, name='sync_antenna_api'),
]
