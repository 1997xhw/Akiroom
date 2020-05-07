import datetime
import random

from SmartDjango import models
from smartify import P

from Base.room import RoomError

from User.models import User


class Room(models.Model):
    """
    房间类
    """

    number = models.IntegerField(
        unique=True,
        null=False,
    )
    password = models.CharField(
        max_length=5,
        min_length=4,
        null=True,
        default=None
    )
    owner = models.ForeignKey(
        'Room.member',
        related_name='owner',
        on_delete=models.CASCADE,
    )
    member_a = models.ForeignKey(
        'Room.member',
        related_name='member_a',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
    )
    member_b = models.ForeignKey(
        'Room.member',
        related_name='member_b',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
    )
    # 房间人数0/3
    member_num = models.IntegerField(
        default=1,
    )
    # 轮到说话的人（1、2、3）（1默认房主）
    speaker = models.IntegerField(
        default=1,

    )
    create_time = models.DateTimeField(
        auto_now_add=True
    )

    def d(self):
        return self.dictor('pk->rid', 'number', 'password', 'owner', 'member_a', 'member_b', 'member_num', 'speaker',
                           'creat_time')

    def d_room_list(self):
        return self.dictor('pk->rid', 'number', 'owner', 'member_a', 'member_b', 'member_num',
                           'creat_time')

    def _readable_owner(self):
        if self.owner:
            return self.owner.d()

    def _readable_member_a(self):
        if self.member_a:
            return self.member_a.d()

    def _readable_member_b(self):
        if self.member_b:
            return self.member_b.d()

    def _readable_creat_time(self):
        return self.create_time.timestamp()

    @classmethod
    def check_password(cls, room, password):
        """验证房间密码是否正确"""
        if room.password != None:
            if room.password != password:
                raise RoomError.JOIN_ROOM_PASSWORD(room.number)

    @staticmethod
    def get_room_by_pk(pk):
        try:
            return Room.objects.get(pk=pk)
        except Exception:
            raise RoomError.GET_ROOM_BY_PK(pk)

    @staticmethod
    def get_room_by_number(number):
        try:
            room = Room.objects.get(number=number)
        except Room.DoesNotExist:
            raise RoomError.GET_ROOM_BY_NUMBER(number)
        return room

    @classmethod
    def get_room_list(cls):
        Rooms = []
        for room in Room.objects.filter(create_time__lte=datetime.datetime.now()):
            Rooms.append(room.d_room_list())
        return Rooms

    @classmethod
    def creat_room(cls, user, password):
        try:
            print(password)
            room = cls(
                number=random.randint(1000, 9999),
                owner=member.join_room(user),
                password=password
            )
            room.save()

        except Exception as err:
            user.leave_room()
            raise RoomError.Create_ROOM(debug_message=err)
        return room

    @classmethod
    def join_room(cls, user, room, password):
        Room.check_password(room, password)
        try:
            member_num = room.member_num
            if member_num == 1:
                room.member_a = member.join_room(user)
            else:
                room.member_b = member.join_room(user)
            room.member_num = member_num + 1
            room.save()
        except Exception:
            raise RoomError.MEMBER_JOIN_ROOM(user.username, room.number)
        return room


class RoomP:
    password, number, = Room.get_params('password', 'number')
    room_number = P('number', '房间号', 'room').process(Room.get_room_by_number)
    room_password = P('password', '房间密码')


class member(models.Model):
    user = models.ForeignKey(
        'User.User',
        on_delete=models.CASCADE,
    )
    # 是否准备
    is_ready = models.BooleanField(
        default=False
    )

    def d(self):
        return self.dictor('pk->mid', 'user', 'is_ready')

    def _readable_user(self):
        if self.user:
            return self.user.d()

    def ready(self):
        self.is_ready = True
        self.save()

    def unready(self):
        self.is_ready = False
        self.save()

    @classmethod
    def join_room(cls, user):
        print("######user:" + user.username + "___join_room")
        try:
            member = cls(
                user=user,
            )
            member.save()
        except Exception:
            raise RoomError.JOIN_ROOM(user.username)
        user.entered_room()
        return member


class action(models.Model):
    member = models.ForeignKey(
        'Room.member',
        on_delete=models.CASCADE
    )
    content = models.TextField(
        default=None,
        null=True
    )
    create_time = models.DateTimeField(
        auto_now_add=True
    )
