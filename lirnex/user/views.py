from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.views.generic import FormView, DetailView, ListView, View, UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.db.models import Q



from user import models
from basic.models import Post
from .forms import CustomUserCreationForm, ProfileForm

from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer

# Список всех профилей и создание нового
class ProfileListAPI(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# Детали одного профиля по ID
class ProfileDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class SubscribeView(LoginRequiredMixin, View):
    def post(self, request, username, *args, **kwargs):
        target_user = get_object_or_404(User, username=username)
        if target_user != request.user:
            request.user.profile.following.add(target_user.profile)
        return redirect('user:profile', username=username)

class UnsubscribeView(LoginRequiredMixin, View):
    def post(self, request, username, *args, **kwargs):
        target_user = get_object_or_404(User, username=username)
        if target_user != request.user:
            request.user.profile.following.remove(target_user.profile)
        return redirect('user:profile', username=username)

class ProfileView(DetailView):
    model = models.Profile
    template_name = "user/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        username = self.kwargs.get("username") 
        return get_object_or_404(models.Profile, user__username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.object.user).order_by('-created_at')
        context['is_owner'] = self.request.user == self.object.user
        return context
    

# my profile
def my_profile_redirect(request):
    if not request.user.is_authenticated:
        return redirect("user:login")
    return redirect("user:profile", username=request.user.username)



class RegisterView(FormView):
    template_name = "user/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("basic:home")

    def form_valid(self, form):
        user = form.save()
        models.Profile.objects.create(user=user)
        login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = "user/login.html"
    authentication_form = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy("basic:home") 


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("user:login")

class SearchUsersView(ListView):
    model = models.Profile
    template_name = 'user/search_users.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return models.Profile.objects.filter(
                Q(user__username__icontains=query) |
                Q(bio__icontains=query)
            )
        return models.Profile.objects.none()  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'user/update_profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        # Просто указываем URL профиля напрямую
        return reverse_lazy('user:profile', kwargs={'username': self.request.user.username})

def followers_list(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    return render(request, "partials/user_list.html", {
        "users": profile.followers.all()
    })

def following_list(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    return render(request, "partials/user_list.html", {
        "users": profile.following.all()
    })
