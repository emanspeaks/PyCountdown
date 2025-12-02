from pyrandyos.utils.json import parse_jsonc
from pyrandyos.utils.casesafe import (
    casesafe_dict_get, casesafe_key_in_dict, casesafe_value_in_container,
    casesafe_is_equal,
)

from .clocks import Clock, DEFAULT_CLOCKS
from .timeutils import now_tai_sec, ymdhms_to_sec
from ..logging import log_error


class DisplayClock:
    pool: list['DisplayClock'] = list()

    def __init__(self, label: str, clk: Clock, hidden: bool = False) -> None:
        self.label = label
        self.clock = clk
        self.hidden = hidden

    @classmethod
    def add_to_pool(cls, dclk: 'DisplayClock' = None,
                    insert_before_idx: int = -1):
        pool = cls.pool
        dclk = dclk or Clock(DEFAULT_CLOCKS['TAI'], now_tai_sec())
        if insert_before_idx < 0:
            pool.append(dclk)

        else:
            pool.insert(insert_before_idx, dclk)

    @classmethod
    def remove_from_pool(cls, idx: int):
        cls.pool.pop(idx)

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
    def get_clock_by_name(cls, name: str):
        if casesafe_key_in_dict(DEFAULT_CLOCKS, name, True):
            return casesafe_dict_get(DEFAULT_CLOCKS, name, None, True)
        poolnames = cls.get_pool_names()
        if casesafe_value_in_container(poolnames, name, True):
            for i, x in enumerate(poolnames):
                if casesafe_is_equal(x, name, True):
                    return cls.pool[i].clock

    @classmethod
    def from_jsonc(cls, data: str | list[dict]):
        if isinstance(data, str):
            data = parse_jsonc(data)

        pool = cls.pool
        if data:
            pool.clear()

        for row in data:
            label = row['label']
            clockkey = row['clock']
            clock = cls.get_clock_by_name(clockkey)
            if not clock:
                log_error(f"invalid clock name: {clockkey}.  Skipping entry.")
                continue

            epoch = row.get('epoch')
            if isinstance(epoch, list):
                epoch = ymdhms_to_sec(*epoch)

            if epoch is not None:
                clock = Clock(clock, epoch)

            hidden = row.get('hidden', False)
            cls.add_to_pool(cls(label, clock, hidden))
