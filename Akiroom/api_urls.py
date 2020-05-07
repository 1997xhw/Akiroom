from django.urls import path, include


urlpatterns = [
    path('/base', include('Base.api_urls')),
    path('/user', include('User.api_urls')),
    path('/room', include('Room.api_urls')),

]
