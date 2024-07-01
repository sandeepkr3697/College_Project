from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('encryption/', views.encryption, name='encryption'),
    path('encryption_success/<str:image_path>/', views.encryption_success, name='encryption_success'),
    path('decryption/', views.decryption, name='decryption'),
    path('decryption_success/<str:received_message>/', views.decryption_success, name='decryption_success'),
]

