from SmartDjango import E


@E.register()
class RoomError:
    Create_ROOM = E("创建房间失败")
    JOIN_ROOM = E("用户{0}加入房间失败")
class Room:
    pass
