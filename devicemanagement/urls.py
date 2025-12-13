from django.contrib import admin
from django.urls import path, include
from accounts.views import LoginUserView, RefreshTokenViewCustom, LogoutUserView, RegisterUserView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/',include('accounts.urls')),

    path('api/auth/login/', LoginUserView.as_view(), name='login'),
    path('api/auth/refresh/', RefreshTokenViewCustom.as_view(), name='refresh'),
    path('api/auth/logout/', LogoutUserView.as_view(), name='logout'),
    path('api/auth/register/', RegisterUserView.as_view(), name='register'),

    path('api/leader/', include('accounts.leader_urls')),
    path('api/leader/devices/', include('devices.urls')),  

    path('api/employee/', include('accounts.employee_urls')),

    path('api/devices/', include('devices.employee_urls')),

    path('api/leader/',include('devices.urls')),
    path('api/employee/',include('devices.urls')),
]
