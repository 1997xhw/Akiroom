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
    is_public = models.BooleanField(
        default=True
    )
    owner = models.ForeignKey(
        'Room.Member',
        related_name='owner',
        on_delete=models.SET_NULL,
        null=True,
    )
    member_a = models.ForeignKey(
        'Room.Member',
        related_name='member_a',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
    )
    member_b = models.ForeignKey(
        'Room.Member',
        related_name='member_b',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
    )
    # 房间人数0/3
    member_num = models.IntegerField(
        default=1,
    )

    status = models.BooleanField(
        default=False
    )

    # 轮到说话的人（1、2、3）（1默认房主）
    speaker = models.IntegerField(
        default=1,

    )
    create_time = models.DateTimeField(
        auto_now_add=True
    )

    def d(self):
        return self.dictor('pk->rid', 'is_public', 'number', 'password', 'owner', 'member_a', 'member_b', 'member_num',
                           'speaker', 'status',
                           'create_time')

    def d_room_list(self):
        return self.dictor('pk->rid', 'number', 'is_public', 'owner', 'member_a', 'member_b', 'member_num',
                           'create_time')

    def d_number(self):
        return self.dictor('number')

    def _readable_owner(self):
        if self.owner:
            return self.owner.d()

    def _readable_member_a(self):
        if self.member_a:
            return self.member_a.d()

    def _readable_member_b(self):
        if self.member_b:
            return self.member_b.d()

    def _readable_create_time(self):
        return self.create_time.timestamp()

    @classmethod
    def check_password(cls, room, password):
        """验证房间密码是否正确"""
        if not room.is_public:
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
                owner=Member.join_room(user),
                password=password
            )
            if room.password is not None:
                room.is_public = False
            room.save()

        except Exception as err:
            user.leave_room()
            raise RoomError.Create_ROOM(debug_message=err)
        return room

    @classmethod
    def close_room(cls, room):
        try:
            if room.member_a is not None:
                Member.leave_room(room.member_a)
            if room.member_b is not None:
                Member.leave_room(room.member_b)
            if room.owner is not None:
                Member.leave_room(room.owner)
            room.delete()
            print("delete======ok")
        except Exception as err:
            raise RoomError.CLOSE_ROOM(room.number, debug_message=err)

    @classmethod
    def join_room(cls, user, room, password):
        Room.check_password(room, password)
        if room.member_num == 3:
            raise RoomError.ROOM_FULL(room.number)
        try:
            member_num = room.member_num
            if member_num == 1:
                room.member_a = Member.join_room(user)
            else:
                room.member_b = Member.join_room(user)
            room.member_num = member_num + 1
            room.save()
        except Exception:
            raise RoomError.MEMBER_JOIN_ROOM(user.username, room.number)
        return room

    @classmethod
    def change_position(cls, room):
        if room.owner is None:
            if room.member_b is not None:
                print("b->owner")
                room.owner = room.member_b
                room.member_b = None

            elif room.member_a is not None:
                print("a->owner")
                room.owner = room.member_a
                room.member_a = None
        if room.member_a is None and room.member_b is not None:
            print("b->a")
            room.member_a = room.member_b
            room.member_b = None
        room.member_num = room.member_num - 1
        print(room.member_num)
        room.save()
        if room.member_num == 0:
            cls.close_room(room)

    def get_room_member(self):
        return [self.owner, self.member_a, self.member_b]

    @staticmethod
    def room_ready_status(user, room, ready):
        if room.status:
            raise RoomError.ROOM_NOT_UNREADY(room.number)
        try:
            print(ready)
            for member in room.get_room_member():
                if member.user == user:
                    member.is_ready = ready
                    member.save()
            return room
        except Exception as err:
            raise RoomError.ROOM_CHANGE_STATUS(room.number, user.username, debug_message=err)

    @staticmethod
    def room_begin(room):
        room.status = True
        room.save()
        return room

    def room_change_speaker(self):
        try:
            self.speaker = (self.speaker + 1)
            if self.speaker == 4:
                self.speaker = 1
            self.save()
        except Exception:
            raise RoomError.ROOM_CHANGE_SPEAKER(self.number)


class RoomP:
    password, number, = Room.get_params('password', 'number')
    room_number = P('number', '房间号', 'room').process(Room.get_room_by_number)
    room_password = P('password', '房间密码')


class Member(models.Model):
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

    def d_username(self):
        return self.user.d_username()

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

    @classmethod
    def leave_room(cls, user):
        try:
            print("######user:" + user.username + "___leave_room")
            member = Member.objects.get(user=user)
            user.leave_room()
            member.delete()
        except Exception as err:
            raise RoomError.LEAVE_ROOM(debug_message=err)


class Actions(models.Model):
    member = models.ForeignKey(
        'Room.Member',
        on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        'Room.Room',
        on_delete=models.CASCADE,
    )
    content = models.TextField(
        default=None,
        null=True
    )
    create_time = models.DateTimeField(
        auto_now_add=True
    )

    def d(self):
        return self.dictor('pk->aid', 'member', 'room', 'content', 'create_time')

    def _readable_member(self):
        return self.member.d_username()

    def _readable_room(self):
        return self.room.d_number()

    def _readable_create_time(self):
        return self.create_time.timestamp()

    @staticmethod
    def get_actions(room):
        actions = []
        for action in Actions.objects.filter(room=room).order_by("-create_time"):
            actions.append(action.d())
        return actions

    @classmethod
    def create_action(cls, member, content, room):
        if content:
            try:
                action = cls(
                    member=member,
                    room=room,
                    content=content
                )
                action.save()
            except Exception as err:
                raise RoomError.CREATE_ACTION(room.number, member.user.username, debug_message=err)
        room.room_change_speaker()
        return dict(
            next_speaker=room.speaker
        )


class ActionP:
    content = Actions.get_param('content')
