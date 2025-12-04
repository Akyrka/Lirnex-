from django.contrib import admin
from django.urls import include, path
from basic import views  
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = "basic"


urlpatterns = [
    path('', views.BasicHomeView.as_view(), name="home"),
    path("post_create/", views.PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name="post-delete"),
    path("post/<int:pk>/like/", views.LikePostView.as_view(), name="like-post"),
    path("post/<int:pk>/comment/", views.AddCommentView.as_view(), name="add_comment"),
    path('comment/<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path("notifications/", views.NotificationsView.as_view(), name="notifications"),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)