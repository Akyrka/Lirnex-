from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Media
from basic import models
from .forms import PostForm, MediaFormSet
from django.urls import reverse


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'basic/post_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['media_formset'] = MediaFormSet(self.request.POST, self.request.FILES)
        else:
            context['media_formset'] = MediaFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        media_formset = context['media_formset']
        form.instance.author = self.request.user

        # Проверяем форму медиа ДО сохранения поста
        if not media_formset.is_valid():
            return self.form_invalid(form)

        has_file = any(f.cleaned_data.get('file') for f in media_formset.forms if f.cleaned_data)

        if not has_file:
            form.add_error(None, "Неможливо опубліковати пусту публікацію.")
            return self.form_invalid(form)

        # Всё ок — сохраняем пост и файлы
        self.object = form.save()
        media_formset.instance = self.object
        media_formset.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('basic:post_detail', kwargs={'pk': self.object.pk})


    
class PostDetailView(DetailView):
    model =  models.Post
    template_name = "basic/post_detail.html"
    context_object_name = "post"

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Post
    template_name = "basic/confirm_delete.html"
    context_object_name = "post"

    def get_success_url(self):
        return reverse("user:profile", kwargs={"username": self.request.user.username})

class BasicHomeView(ListView):
    model = models.Post
    template_name="basic/home.html"