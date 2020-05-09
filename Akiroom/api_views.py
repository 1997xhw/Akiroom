from SmartDjango import Analyse
from django.views import View
from smartify import P

from Base.auth import Auth
from Base.room import Room as Roomm
from Room.models import RoomP, Room, Member, Actions, ActionP


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

    # @staticmethod
    # @Auth.require_login
    # @Analyse.r(b=[RoomP.room_number])
    # @Roomm.is_room_onwer
    # def delete(request):
    #     """DELETE /api/room
    #
    #     关闭房间
    #     """
    #     Room.close_room(**request.d.dict('room'))


class RoomMemberView(View):
    @staticmethod
    @Auth.require_login
    @Analyse.r(a=[RoomP.room_number])
    @Roomm.is_room_member
    def post(request):
        """POST /api/room/member/@<int:number>
        获取房间信息
        """
        return request.d.room.d()

    @staticmethod
    @Auth.require_login
    @Analyse.r(a=[RoomP.room_number])
    @Roomm.is_room_member
    def delete(request):
        """DELETE /api/room/member/@<int:number>

        退出房间
        """
        room_number = request.d.room.number
        Member.leave_room(request.user)
        Room.change_position(Room.get_room_by_number(room_number))

    @staticmethod
    @Auth.require_login
    @Analyse.r(a=[RoomP.room_number], b=[P('ready', '是否准备').default(True).process(bool)])
    @Roomm.is_room_member
    def put(request):
        """PUT /api/room/member/@<int:number>

        房间状态操作（开始游戏（两人准备）/准备）
        """
        return Room.room_ready_status(request.user, **request.d.dict('room', 'ready')).d()


class RoomMemberOwnerView(View):
    @staticmethod
    @Auth.require_login
    @Analyse.r(a=[RoomP.room_number])
    @Roomm.is_room_owner
    @Roomm.room_status
    def put(request):
        """PUT /api/room/member/owner/@<int:number>

        房主点开始发言
        """
        return Room.room_begin(**request.d.dict('room')).d()

    @staticmethod
    @Auth.require_login
    @Analyse.r(a=[RoomP.room_number])
    @Roomm.is_room_owner
    def delete(request):
        """DELETE /api/room/member/owner/@<int:number>

        关闭房间
        """
        Room.close_room(**request.d.dict('room'))


class RoomActionView(View):
    @staticmethod
    @Auth.require_login
    @Analyse.r(a=[RoomP.room_number])
    @Roomm.is_room_member
    def get(request):
        """POST /api/room/action/<int:number>

        获取发言列表
        """
        return Actions.get_actions(**request.d.dict('room'))

    @staticmethod
    @Auth.require_login
    @Analyse.r(a=[RoomP.room_number], b=[ActionP.content])
    @Roomm.is_room_member
    @Roomm.member_can_act
    def post(request):
        """POST /api/room/action/<int:number>

        发言
        """
        return Actions.create_action(request.member, **request.d.dict('content', 'room'))
