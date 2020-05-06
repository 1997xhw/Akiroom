from SmartDjango import models


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
        default=0,
    )
    # 轮到说话的人（1、2、3）（1默认房主）
    speaker = models.IntegerField(
        default=1,

    )
    create_time = models.DateTimeField(
        auto_now_add=True
    )


class member(models.Model):
    user = models.ForeignKey(
        'User.User',
        on_delete=models.CASCADE,
    )
    # 是否准备
    is_ready = models.BooleanField(
        default=False
    )


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
