from datetime import timezone, timedelta

from .timezone import USTimeZone

JY2DAY = 365.25
DAY2SEC = 86400.0
CY2DAY = JY2DAY*100

UNIX_UTC_SEC = -946728000.0

# from the FreeFlyer documentation:
# * Julian Date: Jan 1 4713 BCE 12:00:00.000 TAI
JDJ2K = 2451545.0
# * MJD GSFC: Jan 05 1941 12:00:00.000 TAI
# used by FreeFlyer
GSFC_MJD = 2430000.0
# * MJD USNO: Nov 17 1858 00:00:00.000 TAI
# used by SOFA and IERS
USNO_MJD = 2400000.5
# * MJD GPS: Jan 06 1980 00:00:00.000 UTC
GPST_EPOCH_TAI = -630763181.0
# * MJD 1950 (Besselian Date 1950.0): Dec 31 1949 22:09:46.862 TAI
M50_EPOCH_TAI_YMDHMS = (1949, 12, 31, 22, 9, 46.862)

YMDHMSKEYS = ('year', 'month', 'day', 'hour', 'minute', 'second')
DAYSINMONTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

# default leap seconds from naif0012.tls
LEAPS_TABLE = [
    10.0, -883656000.0,
    11.0, -867931200.0,
    12.0, -852033600.0,
    13.0, -820497600.0,
    14.0, -788961600.0,
    15.0, -757425600.0,
    16.0, -725803200.0,
    17.0, -694267200.0,
    18.0, -662731200.0,
    19.0, -631195200.0,
    20.0, -583934400.0,
    21.0, -552398400.0,
    22.0, -520862400.0,
    23.0, -457704000.0,
    24.0, -378734400.0,
    25.0, -315576000.0,
    26.0, -284040000.0,
    27.0, -236779200.0,
    28.0, -205243200.0,
    29.0, -173707200.0,
    30.0, -126273600.0,
    31.0, -79012800.0,
    32.0, -31579200.0,
    33.0, 189345600.0,
    34.0, 284040000.0,
    35.0, 394372800.0,
    36.0, 488980800.0,
    37.0, 536500800.0,
]

TT_MINUS_TAI_SEC = 32.184

# The formulation for UNITIM in SPICE depends on a number of kernel pool
# variables set in the leap second kernel file.  The pool variable names
# are all prefixed with `DELTET/`, so variable names referred to below are
# assumed to have this prefix.
#
# The offset between Teph (called ET/TDB in SPICE parlance) and TT
# is a function of the heliocentric orbit of the Earth-Moon barycenter
# (EMB).  As such, the constants `EB`, `M[0]`, and `M[1]` define properties of
# that orbit.
#  - `EB` is the eccentricity of the heliocentric EMB orbit (we call it e)
#  - `M[0]` is the mean anomaly at J2000.0 TT (we call it m0)
#  - `M[1]` is the mean motion (we call it n)
#
# The constant `K` is defined in Moyer Part 2.
#   K = 2*sqrt(mu_sun*a_emb)/c^2
# (from eq. 2 in section 2.1, coefficient of the sin E terms)
#
# Note that the values referenced directly in the text of the paper itself
# differ in their last digit from what is specified here.  Perhaps the paper
# employed rounding while these values are truncated.  Regardless, for
# for consistency with JPL products, we must assume the values as given in the
# leap second kernels.  These values are unlikely to change so as not to break
# backwards compatibility with older kernels.  However, users can supply their
# own values to our `unitim` should they ever need to be different.
#
# Reference:
#   Moyer, T.D., Transformation from Proper Time on Earth to
#   Coordinate Time in Solar System Barycentric Space-Time Frame
#   of Reference, Part 2, Celestial Mechanics 23 (1981), Pages 58-59
MOYER_K = 1.657e-3
EMB_E = 1.671e-2
# The provenance of these exact values in the LSK are unknown at this time
EMB_M0 = 6.239996e0
EMB_N = 1.99096871e-7

TZEAS = USTimeZone('Eastern', 5)
TZCEN = USTimeZone('Central', 6)
TZMTN = USTimeZone('Mountain', 7)
TZPAC = USTimeZone('Pacific', 8)
TZUTC = timezone.utc

MS = timedelta(milliseconds=1)
