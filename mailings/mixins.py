from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class OwnerAccessMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
