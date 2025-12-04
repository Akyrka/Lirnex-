from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMixinCustom:
    login_url = settings.LOGIN_URL

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)