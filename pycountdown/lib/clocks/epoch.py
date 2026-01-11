from typing import TYPE_CHECKING

from pyrandyos.utils.time.base_convert import (
    et_to_tt, tt_to_tai, unix_to_utc, utc_to_tai,
)
from pyrandyos.utils.time.fmt import (
    TimeFormat, sec_as_fmt, sec_as_fmt_str, TimeFormatter,
)
from pyrandyos.utils.time.rate import BaseClockRate, US_DST

if TYPE_CHECKING:
    from .clock import Clock

_SECS = TimeFormat.S
_TT_RATE = BaseClockRate.TT
_TAI_RATE = BaseClockRate.TAI
_UTC_RATE = BaseClockRate.UTC


class Epoch:
    def __init__(self, clock: 'Clock', epoch_sec: float = 0,
                 fold_known: bool = False, fold: bool = False,
                 input_fmt: TimeFormat = _SECS):
        self.clock = clock
        self.epoch_sec = epoch_sec
        self.fold_known = fold_known
        self.fold = fold
        self.input_fmt = input_fmt

    def copy(self):
        return Epoch(self.clock, self.epoch_sec, self.fold_known,
                     self.fold, self.input_fmt)

    def __str__(self):
        return self.as_fmt_str(digits=3)

    def as_fmt_str(self, fmt: TimeFormatter | TimeFormat = None,
                   digits: int = None, zeropad: int = None):
        tmp_digits = 0
        tmp_zeropad = 0
        if isinstance(fmt, TimeFormatter):
            tmp_digits = fmt.digits
            tmp_zeropad = fmt.zeropad
            fmt = fmt.time_format

        elif fmt is None:
            fmt = self.input_fmt

        if digits is not None:
            tmp_digits = digits

        if zeropad is not None:
            tmp_zeropad = zeropad

        return sec_as_fmt_str(self.epoch_sec, fmt, tmp_digits, tmp_zeropad)

    def as_fmt(self, fmt: TimeFormatter | TimeFormat = None,
               digits: int = None):
        t = self.epoch_sec
        fmt = fmt or self.input_fmt
        return sec_as_fmt(t, fmt, digits)

    def to_tai(self, anchor: 'Clock' = None):
        from .clock import TAI_CLOCK
        epoch_sec = self.epoch_sec
        anchor = anchor or self.clock
        if anchor.is_abs():  # is effectively a base (may be an offset clock)
            rate = anchor.rate

            # clock is at base, convert epoch to tai
            if rate is _TAI_RATE:
                return Epoch(TAI_CLOCK, epoch_sec)

            if rate is BaseClockRate.T_EPH:
                epoch_sec = et_to_tt(epoch_sec)
                rate = _TT_RATE

            if rate is _TT_RATE:
                return Epoch(TAI_CLOCK, tt_to_tai(epoch_sec))

            if rate is BaseClockRate.UNIX:
                epoch_sec = unix_to_utc(epoch_sec)
                rate = _UTC_RATE

            if rate in US_DST:
                fold_known = self.fold_known
                fold = self.fold
                epoch_sec = US_DST[rate][0](epoch_sec, fold, fold_known)
                rate = _UTC_RATE

            if rate is _UTC_RATE:
                return Epoch(TAI_CLOCK, utc_to_tai(epoch_sec))

            raise ValueError("unknown clock rate")

        return Epoch(TAI_CLOCK, epoch_sec + anchor.epoch.to_tai().epoch_sec)

    def plus_seconds(self, dt_sec: float):
        return Epoch(self.clock, self.epoch_sec + dt_sec, self.fold_known,
                     self.fold, self.input_fmt)

    # def wrt_clock(self, clock: 'Clock'):
    #     my_tai = self.to_tai()
    #     clock_tai = clock.epoch_to_tai()
    #     return my_tai - clock_tai
