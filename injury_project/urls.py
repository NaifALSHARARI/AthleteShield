from django.contrib import admin
from django.urls import path
from training_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.player_list, name='player_list'),
    path('add/', views.player_add, name='player_add'),
    path('player/<int:pk>/', views.player_detail, name='player_detail'),
    path('player/<int:pk>/delete/', views.player_delete, name='player_delete'),
    path('reports/', views.reports, name='reports'),
    path('tests/', views.tests, name='tests'),  

    path('recovery-plans/', views.recovery_plans, name='recovery_plans'),  


]
