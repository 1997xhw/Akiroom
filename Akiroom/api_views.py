from SmartDjango import Analyse
from django.views import View
from smartify import P
from Base.auth import Auth
from Room.models import RoomP, Room


class RoomView(View):
    @staticmethod
    @Auth.require_login
    @Auth.is_enter_room
    @Analyse.r(b=[RoomP.password])
    def post(request):
        """POST /api/room/

        创建房间
        """

        return Room.creat_room(request.user, **request.d.dict()).d()

