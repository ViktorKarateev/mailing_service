from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class OwnerAccessMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user

        if obj.owner == user:
            return super().dispatch(request, *args, **kwargs)

        if user.groups.filter(name='Менеджеры').exists():
            if request.method in ('GET', 'HEAD'):
                return super().dispatch(request, *args, **kwargs)
            raise PermissionDenied("Менеджерам запрещено изменять чужие объекты.")

        raise PermissionDenied("Доступ запрещён.")
