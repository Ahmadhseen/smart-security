from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_antenna/', views.add_antenna, name='add_antenna'),
    path('delete_antenna/<int:pk>/', views.delete_antenna, name='delete_antenna'),
    path('edit_antenna/<int:pk>/', views.edit_antenna, name='edit_antenna'),
    path('view_towers/', views.view_towers, name='view_towers'),
    path('add_tower/', views.add_tower, name='add_tower'),
    path('delete_tower/<int:pk>/', views.delete_tower, name='delete_tower'),
    path('edit_tower/<int:pk>/', views.edit_tower, name='edit_tower'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('api/antenna-status/<int:pk>/', views.antenna_status_api, name='antenna_status_api'),
]
