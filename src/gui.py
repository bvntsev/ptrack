import timedelta


def td_from_isoformat(isoformat: str):
    return timedelta(
        hours=int(isoformat[:2]),
        minutes=int(isoformat[3:5]),
        seconds=int(isoformat[6:]),
    )


def unnecessery_zero(num):
    return str(num) if num >= 10 else '0' + str(num)


def isoformat_from_td(td: timedelta):
    td_sec = int(td.total_seconds())
    hours = unnecessery_zero(td_sec // 3600)
    minutes = unnecessery_zero(td_sec // 60 % 60)
    seconds = unnecessery_zero(
        td_sec - td_sec // 3600 * 3600 - td_sec // 60 % 60 * 60
    )
    return f'{hours}:{minutes}:{seconds}'
