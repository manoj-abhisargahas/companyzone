from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.EmployeeInsertView.as_view(), name='newemployee_url'),
    path('view/', views.viewEmployees, name='viewemployees_url'),
    path('view/<int:emp_no>/', views.viewDetailEmployee, name='viewdetailemployee_url'),
    path('update/<int:emp_no>/', views.updateEmployee, name='updateemployee_url'),
    path('delete/', views.deleteEmployee, name='deleteemployee_url'),
    path('viewdeptstats/', views.viewDeptStats, name='viewdeptstats_url'),
]