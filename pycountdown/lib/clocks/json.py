from pyrandyos.utils.json import parse_jsonc
from pyrandyos.utils.casesafe import (
    casesafe_dict_get, casesafe_value_in_container, casesafe_is_equal,
)
from pyrandyos.utils.time.gregorian import ymdhms_to_sec
from pyrandyos.utils.time.dhms import dhms_to_sec
from pyrandyos.utils.time.rate import BaseClockRate
from pyrandyos.utils.time.fmt import (
    TimeFormatter, TimeFormat, parse_time_format,
)

from ...logging import log_error

from .clock import Clock, DEFAULT_CLOCKS
from .displayclocks import DisplayClock
from .epoch import Epoch


JsonEpochTimeType = float | int | list[float | int]
_SECS = TimeFormat.S
CLOCK_NOT_FOUND = object()
CLOCK_UNRESOLVED = object()


def clock_has_problems(clock: Clock | None):
    return clock is CLOCK_NOT_FOUND or clock is CLOCK_UNRESOLVED


def is_clock_resolved(clock: Clock | None):
    return clock is not CLOCK_UNRESOLVED


def handle_clock_problems(clock: Clock | None, json: str):
    if clock is CLOCK_NOT_FOUND:
        log_error(f"Clock not found: {json}")

    return clock_has_problems(clock)


def get_clock_by_id(clk_id: str, pool: list[DisplayClock],
                    id2idx: dict[str, int], label_list: list[str] = None):
    if clk_id is None:
        return

    idx = casesafe_dict_get(id2idx, clk_id, None, True)
    if (idx is None and label_list
            and casesafe_value_in_container(label_list, clk_id, True)):
        for i, x in enumerate(label_list):
            if casesafe_is_equal(x, clk_id, True):
                idx = i
                break

    if idx is not None:
        dclk = pool[idx]
        if dclk:
            return dclk.clock

    clock = casesafe_dict_get(DEFAULT_CLOCKS, clk_id, CLOCK_NOT_FOUND, True)
    if clock is CLOCK_NOT_FOUND and idx is not None:
        return CLOCK_UNRESOLVED
    return clock


def extract_clock_ids(data: list[dict]):
    label_list: list[str] = list()
    id_list: list[str] = list()
    id2idx: dict[str, int] = dict()
    for i, row in enumerate(data):
        # blank = row.get('blank')
        label = row.get('label')
        clk_id = row.get('id', label)
        label_list.append(label)
        id_list.append(clk_id)
        if clk_id:
            id2idx[clk_id] = i

    return label_list, id_list, id2idx


def parse_rate(input_rate: str, follow: Clock = None):
    if input_rate is None:
        input_rate = follow.rate.name if follow else 'TAI'

    return BaseClockRate[input_rate.upper()]


def parse_epoch_time(t: JsonEpochTimeType,
                     input_fmt: TimeFormat = _SECS):
    if isinstance(t, list):
        epochlen = len(t)
        if epochlen == 4 or (epochlen == 5
                             and input_fmt is TimeFormat.DHMS):
            return dhms_to_sec(*t), TimeFormat.DHMS

        elif epochlen == 6:
            return ymdhms_to_sec(*t), TimeFormat.YMDHMS

        else:
            raise NotImplementedError

    elif t is not None:
        return float(t), input_fmt
    return None, input_fmt


def parse_epoch(data: dict, pool: list[DisplayClock], id2idx: dict[str, int],
                label_list: list[str] = None):
    if data is None:
        return

    clockname: str = data['clock']  # data.get('clock') or data.get('anchor')
    clock = get_clock_by_id(clockname, pool, id2idx, label_list)
    if clock_has_problems(clock):
        return clock
    t, fmt = parse_epoch_time(data['t'],
                              parse_time_format(data.get('format', 's')))
    fold_known: bool = data.get('dst_known', False)
    fold: bool = data.get('fold', False)
    return Epoch(clock, t, fold_known, fold, fmt)


def parse_display(data: dict):
    if data is None:
        return

    hidden = data.get('hidden', False)
    fmt = parse_time_format(data.get('format'))
    digits: int = data.get('digits', 0)
    zeropad: int = data.get('zeropad', 0)
    return TimeFormatter(hidden, fmt, digits, zeropad)


def parse_clocks_jsonc(data: str | dict):
    if isinstance(data, str):
        data: dict = parse_jsonc(data)

    data: list[dict] = data['clocks']

    # first get names and IDs of all clocks
    label_list, id_list, id2idx = extract_clock_ids(data)
    ids_to_resolve = list(enumerate(id_list))
    last_to_resolve = None
    dclk_to_add: list[DisplayClock] = [None]*len(data)

    while ids_to_resolve:
        if last_to_resolve == ids_to_resolve:
            log_error(f"Unresolved clocks: {ids_to_resolve}")
            break

        last_to_resolve = ids_to_resolve.copy()
        for resolve_tmp in ids_to_resolve.copy():
            i, clk_id = resolve_tmp
            row = data[i]
            if clk_id is None and row.get('blank'):
                ids_to_resolve.remove(resolve_tmp)
                continue

            label = label_list[i]

            json_follow = row.get('follow')
            follow = get_clock_by_id(json_follow, dclk_to_add, id2idx,
                                     label_list)
            if handle_clock_problems(follow, json_follow):
                continue

            rate = parse_rate(row.get('rate'), follow)

            json_epoch: dict = row.get('epoch')
            epoch = parse_epoch(json_epoch, dclk_to_add, id2idx,
                                label_list)
            if handle_clock_problems(epoch,
                                     json_epoch.get('clock') if json_epoch
                                     else None):
                continue

            json_ref: dict = row.get('ref')
            ref = parse_epoch(json_ref, dclk_to_add, id2idx, label_list)
            if handle_clock_problems(ref,
                                     json_ref.get('clock') if json_ref
                                     else None):
                continue

            # future work
            offset_sec = None
            _abs = False

            clock = Clock(epoch, ref, follow, rate, offset_sec, _abs)

            display_fmt = parse_display(row.get('display')) or TimeFormatter()
            dclk_to_add[i] = DisplayClock(clk_id, label, clock, display_fmt)

            ids_to_resolve.remove(resolve_tmp)

    return dclk_to_add
