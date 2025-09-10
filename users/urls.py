from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('authorize/', views.connect_gmail, name='authorize'),
    path('oauth2callback/', views.oauth2_callback, name='oauth2_callback'),
    path('category/<str:category_name>/', views.category_view, name='category_view'),  # NEW
]
