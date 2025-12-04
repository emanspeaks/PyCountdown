from enum import Enum, auto

from .timeutils import (
    et_to_tt, tt_to_et,
    tt_to_tai, tai_to_tt,
    utc_to_tai, tai_to_utc,
    unix_to_utc, utc_to_unix,
    eastern_to_utc, central_to_utc, mountain_to_utc, pacific_to_utc,
    utc_to_eastern, utc_to_central, utc_to_mountain, utc_to_pacific,
    sec_to_dhms_str, sec_to_ymdhms_str, format_number, sec_to_ydhms_str
)
from .timeconsts import GPST_EPOCH_TAI, UNIX_UTC_SEC, DAY2SEC


class TimeFormat(Enum):
    SECS = 's'
    MINS = 'm'
    HOURS = 'h'
    DAYS = 'd'
    DHMS = 't'  # T as in T-Minus
    YDHMS = 'g'  # short for "GMT day"
    YMDHMS = 'c'  # short for "calendar"
    # ISO = 'i'


class BaseClockRate(Enum):
    UNIX = auto()
    "Ticks with UTC (folds with UTC leaps); starts prior to beginning of UTC"
    UTC = auto()
    "Ticks with TAI, but stretches/folds with leaps"
    TAI = auto()
    "No leap seconds, ticks with TT but fixed offset for historical reasons"
    TT = auto()
    "No leap seconds"
    T_EPH = auto()
    "SPICE relativistic time, ET = JPL T_eph = SPICE TDB"
    US_ET = auto()
    """
    Tick with UTC, folds with UTC leaps, and folds with DST.
    Combines EST and EDT into one clock.
    """
    US_CT = auto()
    """
    Tick with UTC, folds with UTC leaps, and folds with DST.
    Combines CST and CDT into one clock.
    """
    US_MT = auto()
    """
    Tick with UTC, folds with UTC leaps, and folds with DST.
    Combines MST and MDT into one clock.
    """
    US_PT = auto()
    """
    Tick with UTC, folds with UTC leaps, and folds with DST.
    Combines PST and PDT into one clock.
    """


US_DST = {
    BaseClockRate.US_ET: (eastern_to_utc, utc_to_eastern),
    BaseClockRate.US_CT: (central_to_utc, utc_to_central),
    BaseClockRate.US_MT: (mountain_to_utc, utc_to_mountain),
    BaseClockRate.US_PT: (pacific_to_utc, utc_to_pacific),
}


class Clock:
    def __init__(self, anchor: 'Clock', epoch_sec: float = 0,
                 epoch_dst_known: bool = False, epoch_fold: bool = False,
                 input_fmt: TimeFormat = TimeFormat.SECS,
                 rate: BaseClockRate = BaseClockRate.TAI,
                 offset_sec: float = 0,
                 _dst_alt_clk: 'Clock' = None, _abs: bool = False):
        self._tai_cache = None
        self.anchor = anchor
        self.epoch_dst_known = epoch_dst_known
        self.epoch_fold = epoch_fold
        self.epoch_sec = epoch_sec
        self.input_fmt = input_fmt
        self.rate = rate
        self.offset_sec = offset_sec
        self._dst_alt_clk = _dst_alt_clk
        self._abs = _abs

    def is_abs(self):
        return self._abs or self.anchor is None or bool(self.offset_sec)

    @property
    def epoch_sec(self):
        return self._epoch_sec

    @epoch_sec.setter
    def epoch_sec(self, value: float):
        self._epoch_sec = value
        self._tai_cache = None if value is None else self.epoch_to_tai(True)

    def epoch_to_tai(self, _force: bool = False):
        cache = self._tai_cache
        if cache is not None and not _force:
            return cache

        anchor = self.anchor
        epoch = self._epoch_sec
        is_base = anchor is None
        # refs_true_abs_base = epoch is None and anchor.anchor is None
        copy_epoch = epoch is None
        if is_base or copy_epoch:
            return

        if anchor.is_abs():  # is effectively a base (may be an offset clock)
            rate = anchor.rate

            # clock is at base, convert epoch to tai
            if rate is BaseClockRate.TAI:
                return epoch

            if rate is BaseClockRate.T_EPH:
                epoch = et_to_tt(epoch)
                rate = BaseClockRate.TT

            if rate is BaseClockRate.TT:
                return tt_to_tai(epoch)

            if rate is BaseClockRate.UNIX:
                epoch = unix_to_utc(epoch)
                rate = BaseClockRate.UTC

            if rate in US_DST:
                fold = self.epoch_fold
                dst_known = self.epoch_dst_known
                epoch = US_DST[rate][0](epoch, fold, dst_known)
                rate = BaseClockRate.UTC

            if rate is BaseClockRate.UTC:
                return utc_to_tai(epoch)

            raise ValueError("unknown clock rate")

        return epoch + anchor.epoch_to_tai()

    def epoch_wrt_clock(self, clock: 'Clock'):
        my_tai = self.epoch_to_tai()
        clock_tai = clock.epoch_to_tai()
        return my_tai - clock_tai

    def cumulative_offset(self):
        anchor = self.anchor
        offset = self.offset_sec
        if anchor:
            offset += anchor.cumulative_offset()
        return offset

    def effective_tai(self, real_tai: float):
        return real_tai - self.cumulative_offset()

    def tai_to_clock_time(self, tai: float):
        offset = self.offset_sec
        eff_tai = self.effective_tai(tai)
        rate = self.rate
        my_epoch = 0 if offset else (self.epoch_to_tai() or 0)
        epoch = eff_tai - my_epoch

        if rate is BaseClockRate.TAI:
            return epoch

        if rate in (BaseClockRate.T_EPH, BaseClockRate.TT):
            epoch = tai_to_tt(epoch)
            if rate is BaseClockRate.TT:
                return epoch
            return tt_to_et(epoch)

        epoch = tai_to_utc(epoch)
        if rate is BaseClockRate.UTC:
            return epoch

        if rate is BaseClockRate.UNIX:
            return utc_to_unix(epoch)

        if rate in US_DST:
            return US_DST[rate][1](epoch)

    def display(self, now_tai: float, fmt: TimeFormat = None,
                sec_digits: int = 0, zeropad: int = 0):
        offset = self.offset_sec
        my_tai = None if offset else self.epoch_to_tai()
        t = self.tai_to_clock_time(now_tai)
        if fmt is None:
            fmt = TimeFormat.YMDHMS if my_tai is None else TimeFormat.DHMS

        if fmt is TimeFormat.SECS:
            return format_number(t, sec_digits, zeropad)
        elif fmt is TimeFormat.MINS:
            return format_number(t/60, sec_digits, zeropad)
        elif fmt is TimeFormat.HOURS:
            return format_number(t/3600, sec_digits, zeropad)
        elif fmt is TimeFormat.DAYS:
            return format_number(t/DAY2SEC, sec_digits, zeropad)
        elif fmt is TimeFormat.DHMS:
            return sec_to_dhms_str(t, sec_digits)
        elif fmt is TimeFormat.YDHMS:
            return sec_to_ydhms_str(t, sec_digits)
        elif fmt is TimeFormat.YMDHMS:
            return sec_to_ymdhms_str(t, sec_digits)


def create_default_clocks():
    utc = Clock(None, rate=BaseClockRate.UTC)
    tai = Clock(None, rate=BaseClockRate.TAI)
    tt = Clock(None, rate=BaseClockRate.TT)
    t_eph = Clock(None, rate=BaseClockRate.T_EPH)

    # est = Clock(utc, -5*3600, _abs=True)
    # cst = Clock(utc, -6*3600, _abs=True)
    # mst = Clock(utc, -7*3600, _abs=True)
    # pst = Clock(utc, -8*3600, _abs=True)

    # edt = Clock(est, 3600, _abs=True)
    # cdt = Clock(cst, 3600, _abs=True)
    # mdt = Clock(mst, 3600, _abs=True)
    # pdt = Clock(pst, 3600, _abs=True)

    # us_et = Clock(est, rate=BaseClockRate.US_ET, _dst_alt_clk=edt, _abs=True)
    # us_ct = Clock(cst, rate=BaseClockRate.US_CT, _dst_alt_clk=cdt, _abs=True)
    # us_mt = Clock(mst, rate=BaseClockRate.US_MT, _dst_alt_clk=mdt, _abs=True)
    # us_pt = Clock(pst, rate=BaseClockRate.US_PT, _dst_alt_clk=pdt, _abs=True)

    us_et = Clock(None, rate=BaseClockRate.US_ET)
    us_ct = Clock(None, rate=BaseClockRate.US_CT)
    us_mt = Clock(None, rate=BaseClockRate.US_MT)
    us_pt = Clock(None, rate=BaseClockRate.US_PT)

    unix = Clock(utc, UNIX_UTC_SEC, rate=BaseClockRate.UNIX)
    gpst = Clock(tai, GPST_EPOCH_TAI)

    return {
        'UTC': utc,

        'US ET': us_et,
        'US CT': us_ct,
        'US MT': us_mt,
        'US PT': us_pt,

        # 'EST': est,
        # 'EDT': edt,
        # 'CST': cst,
        # 'CDT': cdt,
        # 'MST': mst,
        # 'MDT': mdt,
        # 'PST': pst,
        # 'PDT': pdt,

        'GPST': gpst,
        'Unix': unix,
        'TAI': tai,
        'TT': tt,
        'TDT': tt,
        'T_eph': t_eph,
        'TDB': t_eph,
    }


DEFAULT_CLOCKS = create_default_clocks()
