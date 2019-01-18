import datetime

from customapp.models import User

TOKEN_EXPIRE_TIME = datetime.timedelta(minutes=30)


def authenticate(username, password):
    try:
        user = User.objects.get(username=username, password=password)
    except User.DoesNotExist:
        user = User(username=username, password=password)
        user.save()
    return user


def get_user(user_id):
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None







