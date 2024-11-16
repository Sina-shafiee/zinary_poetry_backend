from django.urls import path
from .views import LoginView, LogoutView, RegisterView,UserView


urlpatterns = [
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('register/', RegisterView.as_view(), name='user-register'),
    path('me/', UserView.as_view(), name='user-current'),
]