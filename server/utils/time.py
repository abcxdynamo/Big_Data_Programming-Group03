from datetime import datetime, UTC, timedelta


def utcnow():
    return datetime.now(UTC)


delta = timedelta

