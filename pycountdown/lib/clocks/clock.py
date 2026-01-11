from pyrandyos.utils.time.base_convert import GPST_EPOCH_TAI, UNIX_UTC_SEC
from pyrandyos.utils.time.rate import BaseClockRate, tai_to_rate
from pyrandyos.utils.time.fmt import TimeFormatter

from .epoch import Epoch

_TAI_RATE = BaseClockRate.TAI


class Clock:
    def __init__(self,
                 epoch: Epoch = None, ref: Epoch = None,
                 follow: 'Clock' = None,
                 rate: BaseClockRate = _TAI_RATE,
                 offset_sec: float = None,
                 _abs: bool = False):
        # internal properties
        self._abs = _abs
        self._offset_sec = offset_sec

        # clock state
        self.epoch = epoch
        self.ref = ref
        self.follow = follow
        self.rate = rate

    def copy(self):
        epoch = self.epoch
        ref = self.ref
        return Clock(epoch.copy() if epoch else None,
                     ref.copy() if ref else None,
                     self.follow, self.rate, self._offset_sec, self._abs)

    def is_abs(self):
        follow = self.follow
        return (
            self._abs
            or (follow is not None and follow.is_abs())
            or (self.epoch is None and follow is None)
            or (self.epoch is not None and self.ref is not None)
        )

    def is_offset(self):
        return bool(self.offset_sec)

    @property
    def offset_sec(self):
        tmp = self._offset_sec
        no_offset = tmp is None
        offset = tmp or 0
        epoch = self.epoch
        ref = self.ref
        follow = self.follow
        if epoch:
            if no_offset and ref:
                offset = epoch.to_tai().epoch_sec - ref.to_tai().epoch_sec
            else:
                offset += epoch.clock.offset_sec

        if follow:
            offset += follow.offset_sec

        return offset

    @offset_sec.setter
    def offset_sec(self, value: float):
        self._offset_sec = value

    def tai_to_clock_time(self, tai: float):
        offset = self.offset_sec
        epoch = self.epoch
        rate = self.rate
        eff_tai = offset + tai
        if epoch and not self.is_abs():
            if rate is not _TAI_RATE:
                raise NotImplementedError
            return Epoch(self, eff_tai - epoch.to_tai().epoch_sec)
        return Epoch(self, tai_to_rate(eff_tai, rate))

    def display(self, now_tai: float, fmtr: TimeFormatter):
        t = self.tai_to_clock_time(now_tai)
        return t.as_fmt_str(fmtr)


TAI_CLOCK = Clock(None, rate=_TAI_RATE)


def create_default_clocks():
    utc = Clock(None, rate=BaseClockRate.UTC)
    tai = TAI_CLOCK
    tt = Clock(None, rate=BaseClockRate.TT)
    t_eph = Clock(None, rate=BaseClockRate.T_EPH)

    us_et = Clock(None, rate=BaseClockRate.US_ET)
    us_ct = Clock(None, rate=BaseClockRate.US_CT)
    us_mt = Clock(None, rate=BaseClockRate.US_MT)
    us_pt = Clock(None, rate=BaseClockRate.US_PT)

    unix = Clock(Epoch(utc, UNIX_UTC_SEC), rate=BaseClockRate.UNIX)
    gpst = Clock(Epoch(tai, GPST_EPOCH_TAI))

    return {
        'UTC': utc,

        'US ET': us_et,
        'US CT': us_ct,
        'US MT': us_mt,
        'US PT': us_pt,

        'GPST': gpst,
        'Unix': unix,
        'TAI': tai,
        'TT': tt,
        'TDT': tt,
        'T_eph': t_eph,
        'TDB': t_eph,
    }


DEFAULT_CLOCKS = create_default_clocks()
