from django.urls import path
from .views import EmployeeDeviceView

urlpatterns = [
    path('my/', EmployeeDeviceView.as_view(), name='employee-my-device'),
]
