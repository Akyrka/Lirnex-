from django.urls import path
from .views import CustomLoginView, ProfileUpdateView, RegisterView, UserLogoutView, ProfileView, SearchUsersView, SubscribeView, UnsubscribeView,ProfileListAPI, ProfileDetailAPI
from django.conf import settings
from django.conf.urls.static import static


app_name = "user"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/<str:username>/", ProfileView.as_view(), name = "profile"),
    path('search/', SearchUsersView.as_view(), name='search_users'),
    path('subscribe/<str:username>/', SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe/<str:username>/', UnsubscribeView.as_view(), name='unsubscribe'), 
    path("edit/", ProfileUpdateView.as_view(), name="update_profile"),


    path('api/profiles/', ProfileListAPI.as_view(), name='profiles-list-api'),
    path('api/profiles/<int:pk>/', ProfileDetailAPI.as_view(), name='profile-detail-api'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)