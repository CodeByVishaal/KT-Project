from django.urls import path
from .views import UserRegistration, UserLogin, TestAuthentication, UserUpdate

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('profile/', TestAuthentication.as_view(), name='profile'),
    path('update/', UserUpdate.as_view(), name='update'),
]
