from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add, name='add'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('view_towers/', views.view_towers, name='view_towers'),
    path('add_tower/', views.add_tower, name='add_tower'),
    path('add_tower/', views.add_tower, name='add_tower'),
    path('delete_tower/<int:pk>/', views.delete_tower, name='delete_tower'),
    path('edit_tower/<int:pk>/', views.edit_tower, name='edit_tower'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('log_in/', views.log_in, name='log_in'),
]
