from datetime import datetime, tzinfo, timedelta

HOUR = timedelta(hours=1)
ZERO = timedelta()


class USTimeZone(tzinfo):
    def __init__(self, name: str, std_offset_hr: int):
        self.std_offset = timedelta(hours=-abs(std_offset_hr))

        self.name = name
        basechar = name.strip().upper()[0]
        self.std_name = f'{basechar}ST'
        self.dst_name = f'{basechar}DT'

    def tzname(self, dt: datetime):
        return self.dst_name if self.is_dt_dst(dt) else self.std_name

    def utcoffset(self, dt: datetime):
        return self.std_offset + self.dst(dt)

    def dst(self, dt: datetime):
        return HOUR if self.is_dt_dst(dt) else ZERO

    def is_dt_dst(self, dt: datetime):
        # dt is assumed to be the local time, NOT UTC.
        naive_dt = dt.replace(tzinfo=None)

        year = dt.year
        dst_start_base = datetime(year, 3, 8, 2)
        dst_end_base = datetime(year, 11, 1, 1)

        # isoweekday: 1 = mon, 7 = sat
        dst_start_delta = timedelta(days=7 - dst_start_base.isoweekday())
        dst_end_delta = timedelta(days=7 - dst_end_base.isoweekday())

        dst_start = dst_start_base + dst_start_delta
        dst_end = dst_end_base + dst_end_delta

        # # weekday: 1 = sun, 7 = sat
        # =AND(G11 >= DATE(YEAR(G11), 3,8+MOD(7-WEEKDAY(DATE(YEAR(G11),3,8),1)+1,7)) + 2/24,  # noqa
        #      G11 <  DATE(YEAR(G11),11,1+MOD(7-WEEKDAY(DATE(YEAR(G11),11,1),1)+1,7)) + 1/24)  # noqa

        return naive_dt >= dst_start and naive_dt <= dst_end
