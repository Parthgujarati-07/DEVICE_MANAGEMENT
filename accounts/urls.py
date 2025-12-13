from django.urls import path,include

urlpatterns = [
    path('leader/',include('accounts.leader_urls')),
    path('employees/',include('accounts.employee_urls')),
]
