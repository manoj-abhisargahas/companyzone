import time
import logging
from django.urls import Resolver404, resolve
from django.shortcuts import redirect
from django.conf import settings

# Set up a standard logger instance
logger = logging.getLogger(__name__)

class ReqResTimeLoggingMiddleware:
    def __init__(self, get_response):
        # here get_response is a next Middleware Object or View
        self.get_response = get_response

    def __call__(self, request):
        # Before sending Request to next Middleware or View
        # 1. Start the timer before sending the request to next Middleware or View
        start_time = time.perf_counter()
        
        # Sending Request to next Middleware or View
        # 2. Let the view (or subsequent middleware) process the request
        response = self.get_response(request)

        # Before sending Response to previous Middleware
        # insert additional response and read on front-end
        # Example:
        # response['X-Custom-Header'] = 'MyCustomValue'
        # print(response['X-Custom-Header'])
        # 3. Calculate total duration after the response comes back
        end_time = time.perf_counter()
        duration = end_time - start_time
        duration_ms = duration * 1000 # convert to milliseconds

        # 4. Log the performance metrics to your terminal/log files
        log_message = {
            f"METHOD: {request.method} | "
            f"PATH: {request.path} | "
            f"STATUS: {response.status_code} | "
            f"TIME: {duration_ms:.2f}ms"
        }
        logger.info(log_message)

        # Sending Response to previous called Middleware
        return response

# for Web App logins use:
#   @login_required, LoginRequiredMixin
# for Api logins use:
#   from rest_framework.permissions import AllowAny, IsAuthenticated
#   from rest_framework_simplejwt.authentication import JWTAuthentication
"""
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. EXEMPT THE ADMIN PORTAL COMPLETELY
        # If the URL contains '/admin', stop executing immediately and let Django Admin handle itself
        if request.path_info.startswith('/admin') or 'admin' in request.path:
            return self.get_response(request)
        
        try:
            # 2. Try to match the typed URL against your urls.py patterns
            match = resolve(request.path_info)
            url_name = match.url_name
        except Resolver404:
            # 404 BUG FIX: If the URL doesn't match anything, let it pass through!
            # Django will automatically render the standard 404 page for you.
            return self.get_response(request)
        
         # 3. Open paths that anyone can view without logging in
        exempt_urls = ['login_url']

        # 4. Block unauthenticated guests from accessing existing protected pages
        if not request.user.is_authenticated and url_name not in exempt_urls:
            return redirect(settings.LOGIN_URL)
        
        return self.get_response(request)
"""