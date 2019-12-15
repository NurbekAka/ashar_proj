from django.urls import path
from .views import UserRegistrationView, CabinetView, ActivationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name = 'register'),
    path('activate/<str:uidb64>/<str:token>/', ActivationView.as_view(), name='activation'),
    path('cabinet/<int:pk>/', CabinetView.as_view(), name='cabinet'),
]