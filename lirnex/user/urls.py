from django.urls import path
from .views import CustomLoginView, RegisterView, UserLogoutView, ProfileView, SearchUsersView
from django.conf import settings
from django.conf.urls.static import static


app_name = "user"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/<str:username>/", ProfileView.as_view(), name = "profile"),
    path('search/', SearchUsersView.as_view(), name='search_users'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)