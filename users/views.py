from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from .forms import RegisterForm
from .models import CustomUser


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['email', 'phone', 'avatar', 'country']
    template_name = 'users/profile_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user
