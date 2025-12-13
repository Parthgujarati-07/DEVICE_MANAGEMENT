from django.urls import path
from .views import DeviceCreateView,DeviceDeleteView,DeviceDetailView,DeviceListView,DeviceSerializer,DeviceUpdateView,EmployeeDeviceView

urlpatterns = [
    path('devices/create/',DeviceCreateView.as_view()),
    path('devices/list/',DeviceListView.as_view()),
    path('devices/detail/',DeviceDetailView.as_view()),
    path('devices/<int:pk>/update/',DeviceUpdateView.as_view()),
    path('devices/<int:pk>/delete/',DeviceDeleteView.as_view()),

    path('devices/my/',EmployeeDeviceView.as_view()),
]




