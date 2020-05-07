from SmartDjango import Analyse
from django.views import View
from smartify import P
from Base.auth import Auth
from Base.room import Room as Roomm
from Room.models import RoomP, Room, Member


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

    @staticmethod
    @Auth.require_login
    @Analyse.r(b=[RoomP.room_number])
    @Roomm.is_room_onwer
    def delete(request):
        """DELETE /api/room

        关闭房间
        """
        Room.close_room(**request.d.dict('room'))


class RoomMemberView(View):
    @staticmethod
    @Auth.require_login
    @Analyse.r(b=[RoomP.room_number])
    @Roomm.is_room_member
    def delete(request):
        """DELETE /api/room/member

        退出房间
        """
        Member.leave_room(request.user)
