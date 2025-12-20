from pyrandyos.utils.time.fmt import TimeFormat

from .clock import Clock, DEFAULT_CLOCKS
from .fmt import ClockFormatter

JsonEpochType = float | int | list[float | int]


class DisplayClock:
    pool: list['DisplayClock'] = list()

    def __init__(self, clk_id: str, label: str, clock: Clock,
                 formatter: ClockFormatter):

        self.clk_id = clk_id
        self.label = label
        self.clock = clock
        self.formatter = formatter
        fmt = formatter.time_format
        formatter.time_format = fmt or (TimeFormat.YMDHMS if clock.is_abs()
                                        else TimeFormat.DHMS)

    def display(self, now_tai: float, fmt: ClockFormatter = None):
        return self.clock.display(now_tai, fmt or self.formatter)

    @property
    def hidden(self):
        return self.formatter.hidden

    @classmethod
    def get_pool_names(cls):
        return [x.label for x in cls.pool]

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

    # @classmethod
    # def get_clock_by_name(cls, name: str,
    #                       to_add: list['DisplayClock'] = None):
    #     if casesafe_key_in_dict(DEFAULT_CLOCKS, name, True):
    #         return casesafe_dict_get(DEFAULT_CLOCKS, name, None, True)
    #     poolnames = ([x.label if x else None for x in to_add] if to_add
    #                  else cls.get_pool_names())
    #     if casesafe_value_in_container(poolnames, name, True):
    #         for i, x in enumerate(poolnames):
    #             if casesafe_is_equal(x, name, True):
    #                 dclk = to_add[i] if to_add else cls.pool[i]
    #                 return dclk.clock
