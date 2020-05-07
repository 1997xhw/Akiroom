from SmartDjango import Analyse
from django.views import View
from smartify import P
from Base.auth import Auth
from Room.models import RoomP, Room


class RoomView(View):
    @staticmethod
    @Auth.require_login
    def get(request):
        """GET /api/room/

        获得房间列表
        """
        return dict(
            Rooms=Room.get_room_list()
        )

    @staticmethod
    @Auth.require_login
    @Auth.is_enter_room
    @Analyse.r(b=[RoomP.password])
    def post(request):
        """POST /api/room/

        创建房间
        """

        return Room.creat_room(request.user, **request.d.dict('password')).d()

    @staticmethod
    @Auth.require_login
    @Auth.is_enter_room
    @Analyse.r(b=[RoomP.room_number, RoomP.password])
    def put(request):
        """POST /api/room/

        加入房间
        """
        return Room.join_room(request.user, **request.d.dict()).d()
