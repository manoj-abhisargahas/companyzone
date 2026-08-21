from django.contrib.auth import forms

class StrictStaffAuthenticationForm(forms.AuthenticationForm):
    def clean(self):
        # 1. Run default validation (checks username and password matching)
        cleaned_data = super().clean()
        user = self.user_cache

        # 2. THE BLOCK: If the user is NOT staff, deny access completely
        if user and not user.is_staff:
           raise forms.ValidationError(
              "Access Denied. Only authorized staff members can log into this portal.",
              code = "invalid_login",
           )

        return cleaned_data