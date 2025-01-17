from django.urls import path
from .views import UserRegistration, UserLogin, TestAuthentication, UserUpdate, AdminRegistration, UserManagementView, CreateUserProfileView, UpdateUserProfileView

urlpatterns = [
    path('api/user/register/', UserRegistration.as_view(), name='register'),
    path('api/user/login/', UserLogin.as_view(), name='login'),
    path('api/user/test/', TestAuthentication.as_view(), name='profile'),
    path('api/user/update/', UserUpdate.as_view(), name='update'),
    path('api/register/admin/', AdminRegistration.as_view(), name='admin-register'),
    path('api/user/update/<int:pk>/', UserManagementView.as_view()),
    path('api/user/profile/', CreateUserProfileView.as_view(), name='create-profile'),
    path('api/user/profile/update/', UpdateUserProfileView.as_view(), name='update-profile'),
]
