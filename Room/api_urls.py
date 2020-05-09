from django.urls import path

from Akiroom.api_views import RoomView, RoomMemberView, RoomMemberOwnerView, RoomActionView

urlpatterns = [
    path('', RoomView.as_view()),
    path('/member/@<int:number>', RoomMemberView.as_view()),
    path('/member/owner/@<int:number>', RoomMemberOwnerView.as_view()),
    path('/action/@<int:number>', RoomActionView.as_view())

]
