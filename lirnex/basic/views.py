from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Media
from basic import models
from user.models import Profile
from .forms import PostForm, MediaFormSet
from django.urls import reverse
from django.db.models import Q




# class FriendRecommendationsView(TemplateView):
#     template_name = "basic/home.html"



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
    model = Post
    template_name = "basic/home_page.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Получаем посты пользователей, на которых подписан текущий пользователь"""
        if self.request.user.is_authenticated:
            user_profile = self.request.user.profile
            following_profiles = user_profile.following.all()  # подписки

            # Посты авторов, на которых подписан текущий пользователь
            qs = Post.objects.filter(author__profile__in=following_profiles).order_by('-created_at')

            # Добавляем атрибут liked_by_user для шаблона
            for post in qs:
                post.liked_by_user = post.likes.filter(pk=self.request.user.pk).exists()
            return qs
        else:
            return Post.objects.none()  # если аноним — ничего не показываем

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user_profile = self.request.user.profile
            # Подписки для блока рекомендаций
            context['recommended'] = user_profile.following.all()[:5]
        else:
            context['recommended'] = []

        return context


class LikePostView(View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count()
        })

#Comment
class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        text = request.POST.get("text", "").strip()

        if not text:
            return JsonResponse({"error": "Комментарий пустой"}, status=400)

        # Сохраняем объект в переменную
        comment = models.Comment.objects.create(
            post=post,
            user=request.user,
            text=text
        )

        return JsonResponse({
            "id": comment.id,
            "username": request.user.username,
            "text": comment.text,
            "delete_url": reverse('basic:delete_comment', args=[comment.id])
        })
    
class DeleteCommentView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(models.Comment, pk=pk)
        if comment.user == request.user:
            comment.delete()
            return JsonResponse({"success": True, "comment_id": pk})
        return JsonResponse({"success": False, "error": "Нет прав"}, status=403)
    
class NotificationsView(LoginRequiredMixin, View):
    def get(self, request):
        notifications = request.user.notifications.order_by('-created_at')
        return render(request, "basic/notifications.html", {"notifications": notifications})
