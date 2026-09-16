from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
# Authentication Removed for - list
# Authentication for - retrieve, create, update, partial_update, destroy
router.register('ModelViewSetEmployee', views.ModelViewSetEmployeeAPI, basename='modelviewset_emp_api_url')

urlpatterns = [
    # No need Authentication
    path('Register/', views.RegisterToAPI.as_view(), name='api_register_url'),
    path('Login/', TokenObtainPairView.as_view(), name='api_login_url'),

    # Authentication Removed Temp
    path('CustomEmployee/', views.CustomEmployeeAPI.as_view(), name='cust_emp_api_url'), # for GET_ALL which supports Pagination
    path('NewEmpFormData/', views.NewEmpFormData.as_view(), name='new_emp_form_data_url'),
    path('Employee/', views.EmployeeAPI.as_view(), name='emp_api_url'), # for POST
    path('Employee/<int:pk>/', views.EmployeeModifyAPI.as_view(), name='emp_modifyapi_url'), # for GET_ONE, PUT, DELETE

    # Authenticated
    path('CustomEmployee/<int:pk>/', views.CustomEmployeeModifyAPI.as_view(), name='cust_emp_modifyapi_url'),

    path('', include(router.urls)),
]