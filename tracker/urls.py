from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('edit/<str:app_id>/', views.edit_app, name='edit_app'),
    path('delete/<str:app_id>/', views.delete_app, name='delete_app'),
    path('civil-packs/', views.civil_packs, name='civil_packs'),
    path('civil-packs/edit/<str:pack_id>/', views.edit_civil_pack, name='edit_civil_pack'),
    path('civil-packs/export/', views.export_civil_packs, name='export_civil_packs'),
]
