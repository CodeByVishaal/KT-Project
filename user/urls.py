from django.urls import path
from .views import UserRegistration, UserLogin, TestAuthentication, UserUpdate, AdminRegistration, UserManagementView

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('profile/', TestAuthentication.as_view(), name='profile'),
    path('update/', UserUpdate.as_view(), name='update'),
    path('register/admin/', AdminRegistration.as_view(), name='admin-register'),
    path('user/<int:pk>/', UserManagementView.as_view())
]
