from pyrandyos.utils.time.gregorian import (
    ymdhms_to_sec, doy2md,
    # sec_to_y_doy_hms,
)


def y_doy_hms_to_sec(y: int, doy: int, h: int, m: int, s: float):
    mo, d = doy2md(y, doy)
    return ymdhms_to_sec(y, mo, d, h, m, s)
