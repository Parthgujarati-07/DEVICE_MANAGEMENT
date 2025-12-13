from django.urls import path
from .views import EmployeeCreateView,EmployeeDeleteView,EmployeeDetailView,EmployeeListView,EmployeeUpdateView

urlpatterns = [
    path('employees/create/',EmployeeCreateView.as_view()),
    path('employees/list/',EmployeeListView.as_view()),
    path('employees/',EmployeeDetailView.as_view()),
    path('employees/<int:pk>/update/',EmployeeUpdateView.as_view()),
    path('employees/<int:pk>/delete/',EmployeeDeleteView.as_view()),
]

