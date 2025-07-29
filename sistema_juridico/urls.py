from django.contrib import admin
from django.urls import path, include
from processos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('processos.urls')),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('calendario/', views.calendario_view, name='calendario'),
    path('processos/', views.processos_view, name='processos'),
    path('', views.home_view, name='home'),
    path('financas/', views.financas_view, name='financas'),
    path('eventos/', views.eventos_view, name='eventos'),
]