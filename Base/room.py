from SmartDjango import E
from functools import wraps


@E.register()
class RoomError:
    Create_ROOM = E("创建房间失败")
    JOIN_ROOM = E("用户{0}加入房间失败")
    JOIN_ROOM_PASSWORD = E("加入房间({0}) 错误的密码")
    MEMBER_JOIN_ROOM = E("用户{0} 加入房间({1})失败")
    GET_ROOM_BY_PK = E("房间(id:{0})获取失败")
    GET_ROOM_BY_NUMBER = E("房间号:{0}获取失败")
    NOT_ROOM_OWNER = E("用户({0})不是房间({1})主人")
    NOT_ROOM_MEMBER = E("用户({0})不是房间({1})成员")
    LEAVE_ROOM = E("离开房间失败")
    CLOSE_ROOM = E("关闭房间({0})失败")
    ROOM_FULL = E("房间({0})人已满")
    ROOM_NOT_UNREADY = E("房间({0})已开始")
    ROOM_CHANGE_STATUS = E("房间({0})用户({1})改变状态失败")
    ROOM_STATUS_TRUE = E("房间({0})已经开始发言")
    ROOM_STATUS_FALSE = E("房间({0})还没有开始发言")
    MEMBER_IS_NOT_SPEAKER = E("还没有轮到用户({0})发言")
    CREATE_ACTION = E("房间({0})内用户({1})发言失败")
    ROOM_CHANGE_SPEAKER = E("房间({0})切换发言者失败")

class Room:
    @classmethod
    def is_room_owner(cls, func):
        @wraps(func)
        def wrapper(r, *args, **kwargs):
            if r.user == r.d.room.owner.user:
                return func(r, *args, **kwargs)
            else:
                raise RoomError.NOT_ROOM_OWNER(r.user.username, r.d.room.number)

        return wrapper

    @classmethod
    def is_room_member(cls, func):
        @wraps(func)
        def wrapper(r, *args, **kwargs):
            if (r.d.room.member_a and r.user == r.d.room.member_a.user) or (
                    r.d.room.member_b and r.user == r.d.room.member_b.user) or r.user == r.d.room.owner.user:
                return func(r, *args, **kwargs)
            else:
                raise RoomError.NOT_ROOM_MEMBER(r.user.username, r.d.room.number)

        return wrapper

    @classmethod
    def room_status(cls, func):
        @wraps(func)
        def wrapper(r, *args, **kwargs):
            if r.d.room.status:
                raise RoomError.ROOM_STATUS_TRUE(r.d.room.number)
            return func(r, *args, **kwargs)

        return wrapper

    @classmethod
    def member_can_act(cls, func):
        @wraps(func)
        def wrapper(r, *args, **kwargs):
            if not r.d.room.status:
                raise RoomError.ROOM_STATUS_FALSE(r.room.number)
            if r.d.room.get_room_member()[r.d.room.speaker-1].user == r.user:
                r.member = r.d.room.get_room_member()[r.d.room.speaker-1]
                return func(r, *args, **kwargs)
            raise RoomError.MEMBER_IS_NOT_SPEAKER(r.user.username)
        return wrapper
