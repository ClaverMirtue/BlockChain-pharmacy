from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-supply-chain/', views.create_supply_chain, name='create_supply_chain'),
    path('update-status/<int:pk>/', views.update_supply_chain_status, name='update_supply_chain_status'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='pharmacyapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='signup'), name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
]
