from django.urls import path
from .views import EmployeeProfileView

urlpatterns = [
    path('profile/',EmployeeProfileView.as_view()),
]