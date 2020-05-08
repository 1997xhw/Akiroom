from django.urls import path

from Akiroom.api_views import RoomView, RoomMemberView, RoomMemberOwnerView

urlpatterns = [
    path('', RoomView.as_view()),
    path('/member', RoomMemberView.as_view()),
    path('/member/owner', RoomMemberOwnerView())

]
