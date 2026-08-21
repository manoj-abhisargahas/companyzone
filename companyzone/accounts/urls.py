from django.contrib.auth import views as auth_views
from django.urls import path
from .forms import StrictStaffAuthenticationForm

urlpatterns = [
    # For your app users
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        form_class=StrictStaffAuthenticationForm), name='login_url'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login_url'), name='logout_url'),
]