"""
URL configuration for sistema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views as views_app
from cadastro import views as views_cadastro
from login import views as login_views
from painel import views as views_painel 


urlpatterns = [ 
    path('admin/', admin.site.urls),
    #APP
    path('', views_app.home,name='home'),
    path('catalogo/', views_app.catalogo, name='catalogo'),
    path('contato/', views_app.contato, name='contato'),
    path('sobre/', views_app.sobre, name='sobre'),
    path('carrinho/', views_app.loja_carrinho, name='loja_carrinho'),
    path('carrinho/lista/', views_app.lista_carrinho, name='lista_carrinho'),
    path('carrinho/checkout/', views_app.view_checkout, name='view_checkout'),
    path('pedido/sucesso/<int:pedido_id>/', views_app.sucesso_pedido, name='sucesso_pedido'),
    # APP: Rotas de compra e pagamento 
    path('checkout/', views_app.view_checkout, name='view_checkout'),
    path('pedido/<int:pedido_id>/pagamento/', views_app.pagamento_pedido, name='pagamento_pedido'),
    path('pedido/<int:pedido_id>/sucesso/', views_app.sucesso_pedido, name='sucesso_pedido'),
    #Cadastro
    path('cadastro/', views_cadastro.cadastro, name='cadastro'),
    path('ativar-conta/<str:uidb64>/<str:token>/', views_cadastro.ativar_conta, name='ativar_conta'),
    #Login
    path('login/', login_views.login_view, name='login'),
    path('mfa/', login_views.mfa_view, name='mfa'),
    path('logout/', login_views.logout_view, name='logout'),
    path('painel/', login_views.painel_redirect, name='painel'),
    #PAINEL
    path('', views_painel.painel_principal, name='painel_principal'),
    path('admin-gestao/', views_painel.view_administrador, name='view_administrador'),
    path('diretoria/', views_painel.view_diretoria, name='view_diretoria'), 
    path('gerencia-geral/', views_painel.view_gerencia_geral, name='view_gerencia_geral'),
    path('gerencia/', views_painel.view_gerencia, name='view_gerencia'),
    path('supervisao/', views_painel.view_supervisao, name='view_supervisao'),
    path('atendente/', views_painel.view_atendente, name='view_atendente'),
    path('caixa/', views_painel.view_caixa, name='view_caixa'),
    
]
