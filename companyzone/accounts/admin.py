from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser

# Register your models here.

# Registering with UserAdmin ensures password hashing works when you create accounts
# Create a custom layout subclass
class CustomUserAdmin(UserAdmin):
    # This displays the column on the main user listing page
    list_display = ('username', 'is_staff', 'is_api_user')

    fieldsets = UserAdmin.fieldsets + (
        ('Custom API Flags', {
            'fields': ('is_api_user',),
        }),
    )

# Register using your custom layout instead of the default UserAdmin
admin.site.register(AppUser, CustomUserAdmin)