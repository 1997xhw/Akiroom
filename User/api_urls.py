from django.urls import path
from User.api_views import UserView, UsernameView, TokenView, InviteUserView

urlpatterns = [
    path('', UserView.as_view()),
    path('@<str:username>', UsernameView.as_view()),
    path('invite@<str:username>', InviteUserView.as_view()),
    path('token', TokenView.as_view()),
]
