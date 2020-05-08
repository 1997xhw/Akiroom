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
    ROOM_STATUS_TRUE = E("房间({0)已经开始发言")

class Room:
    @classmethod
    def is_room_onwer(cls, func):
        @wraps(func)
        def wrapper(r, *args, **kwargs):
            if r.user == r.room.owner:
                return func(r, *args, **kwargs)
            else:
                raise RoomError.NOT_ROOM_OWNER(r.user.username, r.room.number)

        return wrapper

    @classmethod
    def is_room_member(cls, func):
        @wraps(func)
        def wrapper(r, *args, **kwargs):
            print(r.user.username)
            print(r.d.room.owner.user.username)
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
            if r.room.status:
                raise RoomError.ROOM_STATUS_TRUE(r.room.number)
            return func(r, *args, **kwargs)
        return wrapper
