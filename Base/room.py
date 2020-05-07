from SmartDjango import E


@E.register()
class RoomError:
    Create_ROOM = E("创建房间失败")
    JOIN_ROOM = E("用户{0}加入房间失败")
    JOIN_ROOM_PASSWORD = E("加入房间({0}) 错误的密码")
    MEMBER_JOIN_ROOM = E("用户{0} 加入房间({1})失败")
    GET_ROOM_BY_PK = E("房间(id:{0})获取失败")
    GET_ROOM_BY_NUMBER = E("房间号:{0}获取失败")

class Room:
    pass
