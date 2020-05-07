from django.urls import path

from Akiroom.api_views import RoomView

urlpatterns=[
    path('', RoomView.as_view()),

]
