import datetime

import pytz


def get_now_datetime() -> datetime.datetime:
    return datetime.datetime.now(pytz.timezone("Europe/Moscow")).replace(tzinfo=None)
