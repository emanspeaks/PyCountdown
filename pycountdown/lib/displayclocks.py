from pyrandyos.utils.json import parse_jsonc
from pyrandyos.utils.casesafe import (
    casesafe_dict_get, casesafe_key_in_dict, casesafe_value_in_container,
    casesafe_is_equal,
)

from .clocks import Clock, DEFAULT_CLOCKS, TimeFormat, BaseClockRate
from .timeutils import now_tai_sec, ymdhms_to_sec, dhms_to_sec
from ..logging import log_error

JsonEpochType = float | int | list[float | int]


class DisplayClock:
    pool: list['DisplayClock'] = list()

    def __init__(self, label: str, clk: Clock, hidden: bool = False,
                 time_format: TimeFormat = None, sec_digits: int = 0,
                 zeropad: int = 0) -> None:

        self.label = label
        self.hidden = hidden
        self.sec_digits = sec_digits
        self.zeropad = zeropad

        self.clock = clk
        anchor = clk.anchor
        epoch = clk._epoch_sec
        is_base = anchor is None or epoch is None

        self.time_format = time_format or (TimeFormat.YMDHMS if is_base
                                           else TimeFormat.DHMS)

    def display(self, now_tai: float, fmt: TimeFormat = None,
                sec_digits: int = 0, zeropad: int = 0):
        return self.clock.display(now_tai, fmt or self.time_format,
                                  sec_digits or self.sec_digits,
                                  zeropad or self.zeropad)

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
    def get_clock_by_name(cls, name: str, to_add: list['DisplayClock'] = None):
        if casesafe_key_in_dict(DEFAULT_CLOCKS, name, True):
            return casesafe_dict_get(DEFAULT_CLOCKS, name, None, True)
        poolnames = ([x.label if x else None for x in to_add] if to_add
                     else cls.get_pool_names())
        if casesafe_value_in_container(poolnames, name, True):
            for i, x in enumerate(poolnames):
                if casesafe_is_equal(x, name, True):
                    dclk = to_add[i] if to_add else cls.pool[i]
                    return dclk.clock

    @classmethod
    def from_jsonc(cls, data: str | list[dict]):
        if isinstance(data, str):
            data = parse_jsonc(data)

        pool = cls.pool
        if data:
            pool.clear()

        # first get names of all clocks
        namelist = [row['label'] for row in data]
        to_resolve = list(enumerate(namelist))
        last_to_resolve = None
        to_add = [None]*len(data)

        while to_resolve:
            if last_to_resolve == to_resolve:
                # raise ValueError(f"Unresolved clocks: {to_resolve}")
                log_error(f"Unresolved clocks: {to_resolve}")
                break

            last_to_resolve = to_resolve.copy()
            for i, label in to_resolve.copy():
                label: str
                row = data[i]

                clockname: str = row.get('clock') or row.get('anchor')
                epoch: JsonEpochType = row.get('epoch')
                unit: str = row.get('unit', 's')
                rate: str = row.get('rate', 'TAI')
                epoch_dst_known: bool = row.get('dst_known', False)
                epoch_fold: bool = row.get('fold', False)
                display_format: str = row.get('display_format')
                display_sec_digits: int = row.get('display_sec_digits', 0)
                display_zeropad: int = row.get('display_zeropad', 0)
                offset: str | JsonEpochType = row.get('offset')
                offset_unit: str = row.get('offset_unit', 's')

                clock = cls.get_clock_by_name(clockname, to_add)
                if not clock:
                    # log_error(f"invalid clock name: {clockname}.  Skipping entry.")  # noqa: E501
                    continue

                # coerce input data to correct types
                rate = BaseClockRate[rate.upper()]
                input_fmt = TimeFormat(unit.lower()[0])
                offset_fmt = TimeFormat(offset_unit.lower()[0])
                if display_format:
                    display_format = TimeFormat(display_format.lower()[0])

                epoch, input_fmt = cls.parse_json_epoch(epoch, input_fmt)
                if epoch is not None or clock not in DEFAULT_CLOCKS.values():
                    clock = Clock(clock, epoch, epoch_dst_known, epoch_fold,
                                  input_fmt, rate)

                if isinstance(offset, str):
                    offset_clk = cls.get_clock_by_name(offset, to_add)
                    if not offset_clk:
                        continue
                    offset = offset_clk.epoch_to_tai() - clock.epoch_to_tai()
                elif offset is not None:
                    offset, offset_fmt = cls.parse_json_epoch(offset,
                                                              offset_fmt)

                if offset:
                    clock.offset_sec = offset

                hidden = row.get('hidden', False)
                to_add[i] = cls(label, clock, hidden, display_format,
                                display_sec_digits, display_zeropad)
                to_resolve.remove((i, label))

        for dclk in to_add:
            if dclk:
                cls.add_to_pool(dclk)

    @staticmethod
    def parse_json_epoch(epoch: JsonEpochType,
                         input_fmt: TimeFormat = TimeFormat.SECS):
        if isinstance(epoch, list):
            epochlen = len(epoch)
            if epochlen == 4 or (epochlen == 5
                                 and input_fmt is TimeFormat.DHMS):
                return dhms_to_sec(*epoch), TimeFormat.DHMS

            elif epochlen == 6:
                return ymdhms_to_sec(*epoch), TimeFormat.YMDHMS

            else:
                raise NotImplementedError

        elif epoch is not None:
            return float(epoch), input_fmt
        return None, input_fmt
