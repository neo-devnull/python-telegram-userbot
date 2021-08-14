from .db import Filter, User


def get_message_filters():
    data = {}
    for x in Filter.select():
        cfg = {}
        if x.message_id:
            cfg['message_id'] = x.message_id
        else:
            cfg['reply_text'] = x.reply_text
        data[x.filter_text] = cfg
    return data


def get_users(allowed: bool):
    data = []
    for x in User.select(User.user_id).where(
        User.allowed == allowed
    ):
        data.append(x.user_id)
    return data


def allow_user(user_id: int):
    user = User.select().where(
        User.user_id == user_id
    )

    """
        If user does not exist
        create a new one record
    """
    if not user.count():
        user = User(user_id=user_id,
                    allowed=1,
                    warns=0
                    )
        try:
            user.save()
        except Exception:
            raise
    else:
        user = User.select().where(User.user_id == user_id).get()
        user.warns = 0
        user.allowed = 1
        try:
            user.save()
        except Exception:
            raise


def is_user(user_id: int):
    """
        Check if the user exists in the database
    """
    return User.select().where(User.user_id == user_id).count()
