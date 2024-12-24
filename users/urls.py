from django.urls import path
from users.views import UserLoginView, UserRegistrationView, UserProfileView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    # path('registration/', registration, name='registration'),
    path('registration/',  UserRegistrationView.as_view(), name='registration'),
    # path('profile/', profile, name='profile'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    # path('logout/', logout, name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'), # встроенный Logout

]
