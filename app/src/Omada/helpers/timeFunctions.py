import re
import datetime

__STR_DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
__STR_TIMEDELTA_FORMAT: str = "{days}day(s) {hours}h {minutes}m {seconds}s"


def get_uptime(uptime: str) -> datetime.timedelta:
    pattern = r'(?:(\d+)day\(s\))?\s*(\d+)h\s*(\d+)m\s*(\d+)?s?'
    match = re.match(pattern, uptime)

    if match:
        days = int(match.group(1)) if match.group(1) else 0
        hours = int(match.group(2))
        minutes = int(match.group(3))
        seconds = int(match.group(4)) if match.group(4) else 0

        return datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    return uptime


def get_last_seen(lastSeen: int) -> datetime.datetime:
    lastSeen_seconds = lastSeen / 1000
    return datetime.datetime.fromtimestamp(lastSeen_seconds)


def datetime_to_string(date: datetime.datetime) -> str:
    return date.strftime(__STR_DATETIME_FORMAT)


def timedelta_to_string(timespan: datetime.timedelta) -> str:
    days = timespan.days
    seconds = timespan.seconds

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return __STR_TIMEDELTA_FORMAT.format(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds
    )
