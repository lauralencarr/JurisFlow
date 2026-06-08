from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro_view, name='cadastro'),

    # Dashboard
    path('', views.home_view, name='home'),

    # Processos
    path('processos/', views.processos_view, name='processos'),
    path('processos/<int:pk>/deletar/', views.processo_delete_view, name='processo_delete'),

    # Clientes
    path('clientes/', views.clientes_view, name='clientes'),
    path('clientes/<int:pk>/deletar/', views.cliente_delete_view, name='cliente_delete'),

    # Calendário e Eventos
    path('calendario/', views.calendario_view, name='calendario'),
    path('api/eventos/', views.eventos_api_view, name='eventos_api'),
    path('eventos/criar/', views.evento_criar_view, name='evento_criar'),
    path('eventos/<int:pk>/deletar/', views.evento_delete_view, name='evento_delete'),

    # Finanças
    path('financas/', views.financas_view, name='financas'),
]
