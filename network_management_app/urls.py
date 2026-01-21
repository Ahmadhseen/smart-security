from django.urls import path
from .views import add_tower, dashboard, add, delete_tower, edit, delete, edit_tower, view_towers

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('add/', add, name='add'),
    path('delete/<int:pk>/', delete, name='delete'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('view_towers/', view_towers, name='view_towers'),
    path('add_tower/', add_tower, name='add_tower'),
    path('add_tower/', add_tower, name='add_tower'),
    path('delete_tower/<int:pk>/', delete_tower, name='delete_tower'),
    path('edit_tower/<int:pk>/', edit_tower, name='edit_tower'),
]
