from django.contrib.auth import logout
from django.shortcuts import redirect


class LogoutMixin:
    def logout(self, request):
        logout(request)
        return redirect('index')



