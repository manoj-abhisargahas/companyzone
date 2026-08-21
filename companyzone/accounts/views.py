from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required # Bounces users back to login page if they lack an active session
def dashboard(request):
    res_filename = 'accounts/dashboard.html'
    if request.method == 'GET':
        return render(request, res_filename)