from pyrandyos.utils.time.now import now_tai_sec
from pyrandyos.utils.time.fmt import TimeFormat
from pyrandyos.utils.casesafe import (
    casesafe_dict_get, casesafe_key_in_dict,
    casesafe_value_in_container, casesafe_is_equal,
)

from .epoch import Epoch
from .clock import Clock, DEFAULT_CLOCKS
from .fmt import ClockFormatter

JsonEpochType = float | int | list[float | int]

NOW_ID = '__now'


class DisplayClock:
    pool: list['DisplayClock'] = list()

    def __init__(self, clk_id: str, label: str, clock: Clock,
                 formatter: ClockFormatter):

        self.clk_id = clk_id
        self.label = label
        self.clock = clock
        self.formatter = formatter
        fmt = formatter.time_format
        formatter.time_format = fmt or (TimeFormat.YMDHMS
                                        if clock and clock.is_abs()
                                        else TimeFormat.DHMS)

    def display(self, now_tai: float, fmt: ClockFormatter = None):
        clock = self.clock
        if clock:
            return clock.display(now_tai, fmt or self.formatter)
        return ""

    @property
    def hidden(self):
        return self.formatter.hidden

    @classmethod
    def get_pool_names(cls):
        return [x.label for x in cls.pool]

    @classmethod
    def get_pool_ids(cls):
        return [x.clk_id for x in cls.pool]

    @classmethod
    def get_idx_for_visible_idx(cls, visible_idx: int):
        j = 0
        for i, x in enumerate(cls.pool):
            if x.hidden:
                continue
            if j == visible_idx:
                return i
            j += 1

    @classmethod
    def get_dclock_names_full_list(cls):
        return list(DEFAULT_CLOCKS.keys()) + cls.get_pool_names()

    @classmethod
    def get_dclock_ids_full_list(cls):
        return list(DEFAULT_CLOCKS.keys()) + cls.get_pool_ids()

    @classmethod
    def get_dclock_name_id_full_list(cls):
        return tuple(zip(cls.get_dclock_names_full_list(),
                         cls.get_dclock_ids_full_list()))

    @classmethod
    def dclock_full_list_idx_to_clock(cls, idx: int):
        defaultlen = len(DEFAULT_CLOCKS)
        if idx < defaultlen:
            return DEFAULT_CLOCKS[DEFAULT_CLOCKS.keys()[idx]]
        return cls.pool[idx - defaultlen].clock

    @classmethod
    def get_id_for_clock(cls, clk: Clock):
        for dclk in cls.pool:
            if dclk and dclk.clock is clk:
                return dclk.clk_id
        for k, v in DEFAULT_CLOCKS.items():
            if v is clk:
                return k

    @classmethod
    def get_clock_for_id(cls, clk_id: str):
        if clk_id == NOW_ID:
            return Clock(Epoch(DEFAULT_CLOCKS['TAI'], now_tai_sec()))
        if casesafe_key_in_dict(DEFAULT_CLOCKS, clk_id, True):
            return casesafe_dict_get(DEFAULT_CLOCKS, clk_id, None, True)
        pool_ids = cls.get_pool_ids()
        if casesafe_value_in_container(pool_ids, clk_id, True):
            for i, x in enumerate(pool_ids):
                if casesafe_is_equal(x, clk_id, True):
                    dclk = cls.pool[i]
                    return dclk.clock
