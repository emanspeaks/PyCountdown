from enum import Enum, auto
# from time import time as unixnow


class InputFormat(Enum):
    SECS = auto()
    MINS = auto()
    HOURS = auto()
    DAYS = auto()
    DHMS = auto()
    YDHMS = auto()
    YMDHMS = auto()


class Clock:
    def __init__(self):
        self.epoch_sec = 0
        self.anchor: Clock = None
        self.input_fmt = None
        self._is_dst = False
        self._dst_alt_clk: Clock = None
        # self._utc_cache

    # def sec_wrt_clock(self, clock: 'Clock'):
