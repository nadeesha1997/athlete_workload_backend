from django.urls import path

from authentication.views import UserLoginView, UserProfileView, UserRegistrationView

urlpatterns = [
    path('signup/',UserRegistrationView.as_view()),
    path('login/',UserLoginView.as_view()),
    path('profile/',UserProfileView.as_view()),
    # path('changepassword/',UserChangePasswordView.as_view()),
]