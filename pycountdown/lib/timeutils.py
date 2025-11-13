from time import time as _unixnow
from datetime import datetime, tzinfo
from math import sin

from .timeconsts import (
    MOYER_K, EMB_E, EMB_M0, EMB_N, TT_MINUS_TAI_SEC, GPST_EPOCH_TAI,
    YMDHMSKEYS, TZUTC, TZCEN, TZEAS, TZMTN, TZPAC, LEAPS_TABLE, DAY2SEC,
    DAYSINMONTH, MS, JDJ2K, GSFC_MJD, USNO_MJD, UNIX_UTC_SEC,
)


def emb_kepler(tt: float):
    m = EMB_M0 + EMB_N*tt
    return MOYER_K*sin(m + EMB_E*sin(m))


def et_to_tt(et: float):
    # Since K*M1*(1+EB) is quite small (on the order of 10**-9)
    # 3 iterations should get us as close as we can get to the
    # solution for TDT
    tt = et
    for i in range(3):
        tt = et - emb_kepler(tt)
    return tt


def utc_to_et(utc: float):
    tai = utc_to_tai(utc)
    tt = tai_to_tt(tai)
    return tt_to_et(tt)


def et_to_utc(et: float):
    tt = et_to_tt(et)
    tai = tt_to_tai(tt)
    return tai_to_utc(tai)


def et_to_ut1(et: float, dut1: float):
    utc = et_to_utc(et)
    return utc_to_ut1(utc, dut1)


def tt_to_et(tt: float):
    return tt + emb_kepler(tt)


def tai_to_tt(tai: float):
    return tai + TT_MINUS_TAI_SEC


def tt_to_tai(tt: float):
    return tt - TT_MINUS_TAI_SEC


def tai_to_utc(tai: float, leap: float = None):
    if leap is None:
        leap = get_leaps_at_tai(tai)

    # tai = utc + leap
    return tai - leap


def utc_to_ut1(utc: float, dut1: float):
    return utc + dut1


def tai_to_gpst(tai: float):
    return tai + GPST_EPOCH_TAI


def gpst_to_tai(gpst: float):
    return gpst - GPST_EPOCH_TAI


def utc_to_gpst(utc: float, leap: float = None):
    tai = utc_to_tai(utc, leap)
    return tai_to_gpst(tai)


def gpst_to_utc(gpst: float, leap: float = None):
    tai = gpst_to_tai(gpst)
    return tai_to_utc(tai, leap)


def ymdhms_dict_to_ymdhmsms_dict(ymdhms: dict):
    ymdhmsms = {k: v + 0 for k, v, in ymdhms.items()}
    sec, ms = divmod(ymdhms['second']*1e6, 1e6)
    ymdhmsms['second'] = int(sec)
    ymdhmsms['microsecond'] = int(ms)
    return ymdhmsms


def utc_sec_to_datetime(utc: float):
    dt = ymdhms_dict_to_datetime({k: v for k, v in zip(YMDHMSKEYS,
                                                       sec_to_ymdhms(utc))})
    return dt.replace(tzinfo=TZUTC)


def ymdhms_dict_to_datetime(ymdhms: dict):
    return datetime(**ymdhms_dict_to_ymdhmsms_dict(ymdhms))


def datetime_to_ymdhms(dt: datetime):
    return dt.timetuple()[:6]


def utcoffset(utc: float, tz: tzinfo):
    ymdhms = {k: v for k, v in zip(YMDHMSKEYS, sec_to_ymdhms(utc))}
    utcdt = ymdhms_dict_to_datetime(ymdhms)
    return utcdt.astimezone(tz).utcoffset().total_seconds()


def utc_to_central(utc: float):
    return utc + utcoffset(utc, TZCEN)


def utc_to_eastern(utc: float):
    return utc + utcoffset(utc, TZEAS)


def utc_to_mountain(utc: float):
    return utc + utcoffset(utc, TZMTN)


def utc_to_pacific(utc: float):
    return utc + utcoffset(utc, TZPAC)


def ut1_to_utc(ut1: float, dut1: float):
    return ut1 - dut1


def utc_to_tai(utc: float, leap: float = None):
    if leap is None:
        leap = get_leaps_at_utc(utc)

    # tai = utc + leap
    return utc + leap


def get_leaps_at_utc(utc: float):
    # if the current time equals the timestamp, it means
    # our current "seconds" are ambiguous.  If we had additional information
    # that can distinguish leap seconds, we could do that instead.
    # Since we do not, we are forced to use the same TAI
    # for 23:59:60 and 0:00:00 in this current implementation.

    # for epochs before the first leap second, return delta et at
    # the epoch of the leap second minus one second.
    lastleap = LEAPS_TABLE[0] - 1
    leap = utc*0.0 + lastleap

    for newleap, epoch in zip(LEAPS_TABLE[::2], LEAPS_TABLE[1::2]):
        # tai = utc + leap
        dleap = newleap - lastleap
        leap += (utc >= epoch)*dleap
        lastleap = newleap

    return leap


def get_leaps_at_tai(tai: float):
    # for epochs before the first leap second, return delta et at
    # the epoch of the leap second minus one second.
    lastleap = LEAPS_TABLE[0] - 1
    leap = tai*0.0 + lastleap

    for newleap, epoch in zip(LEAPS_TABLE[::2], LEAPS_TABLE[1::2]):
        # tai = utc + leap
        dleap = newleap - lastleap
        leap += ((tai - newleap) >= epoch)*dleap
        lastleap = newleap

    return leap


def year_is_divisible(year: int, i: float):
    return max(0, 1 + (year//i)*i - abs(year))


def is_leap_year(year: float):
    return (year_is_divisible(year, 4) - year_is_divisible(year, 100)
            + year_is_divisible(year, 400))


def ymdhms_to_sec(y: int, mo: int, d: int, h: int, m: int,
                  s: float):
    # this code is derived from the SPICE TPARSE subroutine.
    # assumes the list is ymdhms format.

    # Get the year month and day as integers.
    year = round(y)
    month = round(mo)
    day = round(d)

    # Apply the Muller-Wimberly formula and then tack on the seconds.
    day = (367*year - (7*(year + ((month + 9)//12))//4)
           - (3*(((year + ((month - 9)//7))//100) + 1)//4)
           + (275*month//9) + day - 730516)

    spj2k = (day - 0.5)*DAY2SEC
    spj2k += 3600.0*h
    spj2k += 60.0*m
    spj2k += s
    return spj2k


def day_of_year(year: int, month: int, day: int):
    """
    gives the number of days that occur before the start of the given month
    """
    x = 0
    for i, d in enumerate(DAYSINMONTH):
        x += d*(i + 1 < month)
    return x + day + is_leap_year(year)*(month > 2)


def doy2md(year: int, doy: int):
    isleap = is_leap_year(year)
    day = doy*1
    month = 0*doy + 1
    tmp = 0
    for i, d in enumerate(DAYSINMONTH):
        d += isleap*(i == 1)
        tmp += d
        filt = doy > tmp
        day -= filt*d
        month += filt*1

    return month, day


def days_from_jan1_1ad_to_jan1(year: int):
    """
    The number of days elapsed since Jan 1, of year 1 A.D., to
    Jan 1 of ``year``
    """
    y = year - 1
    return 365*y + y//4 - y//100 + y//400


def days_past_jan1_1ad(year: int, month: int, day: int):
    return days_from_jan1_1ad_to_jan1(year) + day_of_year(year, month, day) - 1


_J2K_MINUS_J1 = days_past_jan1_1ad(2000, 1, 1)
# noink = 146097 days (400 Gregorian years)
# dwiffle = 36524 days (about 100 years)
# shwiel = 1461 days (about 4 years)
#
# Yes, I know 100 years is a century, but often in astronomical fields,
# a century means a Julian century, which is 36525 days.
# A Gregorian "century" is 36524 days UNLESS the year is divisible by 400,
# in which case it's obviously a noink.  So get over yourself and have fun.
# Probably no one will see this code anyways.
_NOINK = 365*400 + 97
_DWIFFLE = 365*100 + 24
_SHWIEL = 365*4 + 1


def sec_to_ymdhms(formal: float, sec_digits: int = None):
    "returns y, mo, d, h, m, s"
    # this method based on code from SPICE TTRANS

    tmp = formal
    scalar = pow(10, sec_digits or 0)
    if sec_digits is not None:
        tmp = round(tmp*scalar)

    tmp, stmp = divmod(tmp + 43200*scalar, 60*scalar)
    s = stmp/scalar
    tmp, m = divmod(tmp, 60)
    days_past_j2k, h = divmod(tmp, 24)
    days_since_jan1_1ad = days_past_j2k + _J2K_MINUS_J1

    noinks, days_since_last_noink = divmod(days_since_jan1_1ad, _NOINK)
    dwiffles = min(3, days_since_last_noink//_DWIFFLE)

    days_since_last_dwiffle = days_since_last_noink - dwiffles*_DWIFFLE
    shwiels = min(24, days_since_last_dwiffle//_SHWIEL)

    days_since_last_shwiel = days_since_last_dwiffle - shwiels*_SHWIEL
    net_years = min(3, days_since_last_shwiel//365)

    doy = days_since_last_shwiel - net_years*365 + 1
    year = noinks*400 + dwiffles*100 + shwiels*4 + net_years + 1
    month, day = doy2md(year, doy)

    return (int(year), int(month), int(day), int(h), int(m), s)


def dhms_to_sec(d: int, h: int, m: int, s: float):
    return s + 60*m + 3600*h + DAY2SEC*d


def sec_to_dhms(x: float, sec_digits: int = None):
    "returns d, h, m, s"
    d, tmp = divmod(x, DAY2SEC)
    h, tmp = divmod(tmp, 3600)
    scalar = pow(10, sec_digits or 0)
    if sec_digits is not None:
        tmp = round(tmp*scalar)

    m, tmp = divmod(tmp, 60*scalar)
    s = tmp/scalar
    return int(d), int(h), int(m), s


def dhms_to_met_str(d: int, h: int, m: int, s: float):
    dstr = '{:02d}'.format(d)
    hstr = '{:02d}'.format(h)
    mstr = '{:02d}'.format(m)
    sstr = '{:06.3f}'.format(s)
    return dstr + '/' + hstr + ':' + mstr + ':' + sstr


def ymdhms_to_iso(y: int, mo: int, d: int, h: int, m: int,
                  s: float, use_T: bool = True, zone: str = 'Z'):
    ystr = '{:04d}'.format(y)
    mostr = '{:02d}'.format(mo)
    dstr = '{:02d}'.format(d)
    hstr = '{:02d}'.format(h)
    mstr = '{:02d}'.format(m)
    sstr = '{:02.0f}'.format(s)
    tstr = 'T' if use_T else ' '
    return (
        ystr + '-' + mostr + '-' + dstr + tstr
        + hstr + ":" + mstr + ':' + sstr + zone
    )


def datetime_start_end_to_ms(start: datetime, end: datetime):
    return (end - start)/MS


def to_usno_mjd(t_sec_j2k: float):
    return t_sec_j2k/DAY2SEC + (JDJ2K - USNO_MJD)


def to_gsfc_mjd(t_sec_j2k: float):
    return t_sec_j2k/DAY2SEC + (JDJ2K - GSFC_MJD)


def unix_to_utc(unix: float):
    return unix + UNIX_UTC_SEC


def utc_to_unix(utc: float):
    return utc - UNIX_UTC_SEC


def unix_to_central(unix: float):
    utc = unix_to_utc(unix)
    return utc_to_central(utc)


def sec_to_dhms_str(sec: float, sec_digits: int = None):
    return dhms_to_met_str(*sec_to_dhms(sec, sec_digits))


def sec_to_ymdhms_str(sec: float, sec_digits: int = None):
    return ymdhms_to_iso(*sec_to_ymdhms(sec, sec_digits), use_T=False, zone='')


def now_unix_sec():
    return _unixnow()


def now_utc_sec():
    unix = now_unix_sec()
    return unix_to_utc(unix)
