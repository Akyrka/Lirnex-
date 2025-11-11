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
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name="post-delete")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)